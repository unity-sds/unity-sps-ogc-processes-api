import uuid
from datetime import datetime
from typing import Dict

import requests
from fastapi import HTTPException
from fastapi import status as fastapi_status
from jsonschema import ValidationError, validate
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session

from openapi_server.config.config import Settings
from openapi_server.database import crud
from openapi_server.impl.processes_api import ProcessesApiImpl
from openapi_server.utils.redis import RedisLock
from unity_sps_ogc_processes_api.apis.jobs_api_base import BaseJobsApi
from unity_sps_ogc_processes_api.models.execute import Execute
from unity_sps_ogc_processes_api.models.inline_or_ref_data import InlineOrRefData
from unity_sps_ogc_processes_api.models.job_list import JobList
from unity_sps_ogc_processes_api.models.status_code import StatusCode
from unity_sps_ogc_processes_api.models.status_info import StatusInfo


class JobsApiImpl(BaseJobsApi):
    def __init__(
        self, settings: Settings, redis_locking_client: RedisLock, db: Session
    ):
        self.settings = settings
        self.redis_locking_client = redis_locking_client
        self.db = db
        self.ems_api_auth = HTTPBasicAuth(
            settings.EMS_API_AUTH_USERNAME,
            settings.EMS_API_AUTH_PASSWORD.get_secret_value(),
        )

    def check_job_integrity(self, job_id: str, new_job: bool):
        try:
            job = crud.get_job(self.db, job_id)
            if new_job and job is not None:
                raise ValueError
        except crud.NoResultFound:
            if not new_job:
                raise HTTPException(
                    status_code=fastapi_status.HTTP_404_NOT_FOUND,
                    detail=f"Job with ID '{job_id}' not found",
                )
        except crud.MultipleResultsFound:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Multiple jobs found with same ID '{job_id}', data integrity error",
            )
        except ValueError:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Existing job with ID '{job_id}' already exists",
            )
        return job

    def dismiss(self, jobId: str) -> StatusInfo:
        job = self.check_job_integrity(jobId, new_job=False)
        try:
            response = requests.delete(
                f"{self.settings.EMS_API_URL}/dags/{job.processID}/dagRuns/{job.jobID}",
                auth=self.ems_api_auth,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete DAG run {job.jobID} for DAG {job.processID}: {e}",
            )

        crud.delete_job(self.db, job)
        return StatusInfo(
            type="process",
            job_id=jobId,
            status=StatusCode.DISMISSED,
            message="Job dismissed",
            updated=datetime.now(),
        )

    def get_jobs(self) -> JobList:
        jobs = crud.get_jobs(self.db)
        job_status_infos = [StatusInfo.model_validate(job) for job in jobs]
        return JobList(
            jobs=job_status_infos,
            links=[],
        )

    def get_result(self, jobId: str, prefer: str) -> Dict[str, InlineOrRefData]:
        self.check_job_integrity(jobId, new_job=False)
        results = crud.get_results(self.db, jobId)
        return {result.name: InlineOrRefData(href=result.href) for result in results}

    def get_status(self, jobId: str) -> StatusInfo:
        job = self.check_job_integrity(jobId, new_job=False)
        job = StatusInfo.model_validate(job)

        try:
            response = requests.get(
                f"{self.settings.EMS_API_URL}/dags/{job.processID}/dagRuns/{job.jobID}",
                auth=self.ems_api_auth,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch DAG run {job.jobID} for DAG {job.processID}: {e}",
            )

        execution_status_conversion_dict = {
            "queued": StatusCode.ACCEPTED,
            "running": StatusCode.RUNNING,
            "success": StatusCode.SUCCESSFUL,
            "failed": StatusCode.FAILED,
        }
        data = response.json()
        current_execution_status = execution_status_conversion_dict[data["state"]]
        if job.status != current_execution_status:
            job.status = current_execution_status
            job.updated = datetime.now()

        end_date_str = data.get("end_date", None)
        if end_date_str:
            job.finished = datetime.fromisoformat(end_date_str)

        return crud.update_job(self.db, job)

    def execute(self, processId: str, execute: Execute) -> StatusInfo:
        # Fetch process description
        processes_api = ProcessesApiImpl(
            self.settings, self.redis_locking_client, self.db
        )
        process_description = processes_api.get_process(processId)

        # Validate inputs against schema
        validated_inputs = {}
        for input_id, input_value in execute.inputs.items():
            input_description = next(
                (input for input in process_description.inputs if input.id == input_id),
                None,
            )
            if input_description is None:
                raise HTTPException(
                    status_code=fastapi_status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid input: {input_id}",
                )

            try:
                validate(instance=input_value.value, schema=input_description.schema_)
                validated_inputs[input_id] = input_value.value
            except ValidationError as e:
                raise HTTPException(
                    status_code=fastapi_status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid input for {input_id}: {e.message}",
                )

        job_id = str(uuid.uuid4())
        logical_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        data = {
            "dag_run_id": job_id,
            "logical_date": logical_date,
            "conf": validated_inputs,
        }

        try:
            response = requests.post(
                f"{self.settings.EMS_API_URL}/dags/{processId}/dagRuns",
                json=data,
                auth=self.ems_api_auth,
            )
            response.raise_for_status()
            self.check_job_integrity(job_id, new_job=True)
            job = StatusInfo(
                jobID=job_id,
                processID=processId,
                type="process",
                status=StatusCode.ACCEPTED,
                created=datetime.now(),
                updated=datetime.now(),
            )
            return crud.create_job(self.db, job)
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to start DAG run {job_id} with DAG {processId}: {e}",
            )
