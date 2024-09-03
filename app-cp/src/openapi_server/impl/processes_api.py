import uuid
from datetime import datetime

import requests
from fastapi import HTTPException
from fastapi import status as fastapi_status
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session

from openapi_server.config.config import Settings
from openapi_server.database import crud
from openapi_server.impl.dru_api import check_process_integrity
from openapi_server.utils.redis import RedisLock
from unity_sps_ogc_processes_api.apis.processes_api_base import BaseProcessesApi
from unity_sps_ogc_processes_api.models.execute200_response import Execute200Response
from unity_sps_ogc_processes_api.models.execute_workflows import ExecuteWorkflows
from unity_sps_ogc_processes_api.models.process import Process
from unity_sps_ogc_processes_api.models.process_list import ProcessList
from unity_sps_ogc_processes_api.models.process_summary import ProcessSummary
from unity_sps_ogc_processes_api.models.status_code import StatusCode
from unity_sps_ogc_processes_api.models.status_info import StatusInfo


class ProcessesApiImpl(BaseProcessesApi):
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

    def get_process_description(self, processId: str) -> Process:
        process = crud.get_process(self.db, processId)
        return Process.model_validate(process)

    def get_processes(self) -> ProcessList:
        processes = crud.get_processes(self.db)
        return ProcessList(
            processes=[
                ProcessSummary(
                    id=process.id,
                    title=process.title,
                    description=process.description,
                    version=process.version,
                )
                for process in processes
            ],
            links=[],
        )

    def execute(
        self,
        processId: str,
        execute_workflows: ExecuteWorkflows,
        response: str,
        prefer: str,
    ) -> Execute200Response:
        check_process_integrity(self.db, processId, new_process=False)
        job_id = str(uuid.uuid4())
        logical_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        data = {
            "dag_run_id": job_id,
            "logical_date": logical_date,
            "conf": execute_workflows.model_dump(),
        }

        try:
            airflow_response = requests.post(
                f"{self.settings.EMS_API_URL}/dags/{processId}/dagRuns",
                json=data,
                auth=self.ems_api_auth,
            )
            airflow_response.raise_for_status()

            job = StatusInfo(
                jobID=job_id,
                processID=processId,
                type="process",
                status=StatusCode.ACCEPTED,
                created=datetime.now(),
                updated=datetime.now(),
            )
            crud.create_job(self.db, job.model_dump())

            if prefer == "respond-async":
                # Asynchronous execution
                return StatusInfo(
                    type="process",
                    job_id=job_id,
                    status=StatusCode.ACCEPTED,
                    message="Process execution started asynchronously",
                )
            else:
                # Synchronous execution
                # Note: In a real-world scenario, you'd wait for the job to complete
                # and return the actual results. This is a simplified version.
                return Execute200Response(
                    outputs={"result": "Sample output for synchronous execution"}
                )

        except requests.exceptions.RequestException as e:
            status_code_to_raise = fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR
            detail_message = (
                f"Failed to start DAG run {job_id} with DAG {processId}: {str(e)}"
            )

            if hasattr(e, "response"):
                detail_message = f"Failed to start DAG run {job_id} with DAG {processId}: {e.response.status_code} {e.response.reason}"

            raise HTTPException(status_code=status_code_to_raise, detail=detail_message)
