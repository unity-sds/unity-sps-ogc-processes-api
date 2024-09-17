from datetime import datetime
from typing import Dict

import requests
from fastapi import HTTPException, status
from redis.exceptions import LockError

# from jsonschema import ValidationError, validate
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from openapi_server.config.config import Settings
from openapi_server.database import crud
from openapi_server.utils.redis import RedisLock
from unity_sps_ogc_processes_api.apis.jobs_api_base import BaseJobsApi
from unity_sps_ogc_processes_api.models.inline_or_ref_data import InlineOrRefData
from unity_sps_ogc_processes_api.models.job_list import JobList
from unity_sps_ogc_processes_api.models.status_code import StatusCode
from unity_sps_ogc_processes_api.models.status_info import StatusInfo


class JobsApiImpl(BaseJobsApi):
    def __init__(self, settings: Settings, redis_locking_client: RedisLock, db: Session):
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
        except NoResultFound:
            if not new_job:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Job with ID '{job_id}' not found",
                )
        except MultipleResultsFound:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Multiple jobs found with same ID '{job_id}', data integrity error",
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Existing job with ID '{job_id}' already exists",
            )
        return job

    def dismiss(self, jobId: str) -> StatusInfo:
        job_lock_key = f"job:{jobId}"
        try:
            with self.redis_locking_client.lock(job_lock_key):
                job = self.check_job_integrity(jobId, new_job=False)
                process_lock_key = f"process:{job.processID}"
                with self.redis_locking_client.lock(process_lock_key):
                    response = requests.delete(
                        f"{self.settings.EMS_API_URL}/dags/{job.processID}/dagRuns/{job.jobID}",
                        auth=self.ems_api_auth,
                    )
                    response.raise_for_status()
                    crud.delete_job(self.db, job)
                    dismissed_datetime = datetime.now()
                    return StatusInfo(
                        process_id=job.processID,
                        type=job.type,
                        job_id=job.jobID,
                        status=StatusCode.DISMISSED,
                        message="Job dismissed",
                        updated=dismissed_datetime,
                        created=job.created,
                        started=job.started,
                        finished=dismissed_datetime,
                        progress=job.progress,
                        links=job.links,
                    )

        except LockError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to acquire lock. Please try again later.",
            )
        except requests.exceptions.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete DAG run {job.jobID} for DAG {job.processID}: {e}",
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_jobs(self) -> JobList:
        jobs = crud.get_jobs(self.db)
        job_status_infos = [
            StatusInfo(
                process_id=job.processID,
                type=job.type,
                job_id=job.jobID,
                status=job.status,
                message=job.message,
                updated=job.updated,
                created=job.created,
                started=job.started,
                finished=job.finished,
                progress=job.progress,
                links=job.links,
            )
            for job in jobs
        ]
        return JobList(
            jobs=job_status_infos,
            links=[],
        )

    def get_result(self, jobId: str, prefer: str) -> Dict[str, InlineOrRefData]:
        job_lock_key = f"job:{jobId}"
        try:
            with self.redis_locking_client.lock(job_lock_key):
                job = self.check_job_integrity(jobId, new_job=False)
                process_lock_key = f"process:{job.processID}"
                with self.redis_locking_client.lock(process_lock_key):
                    results = crud.get_results(self.db, jobId)
                    return {result.name: InlineOrRefData(href=result.href) for result in results}

        except LockError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to acquire lock. Please try again later.",
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_status(self, jobId: str) -> StatusInfo:
        job_lock_key = f"job:{jobId}"
        try:
            with self.redis_locking_client.lock(job_lock_key):
                job = self.check_job_integrity(jobId, new_job=False)
                process_lock_key = f"process:{job.processID}"
                with self.redis_locking_client.lock(process_lock_key):
                    job = StatusInfo(
                        process_id=job.processID,
                        type=job.type,
                        job_id=job.jobID,
                        status=job.status,
                        message=job.message,
                        updated=job.updated,
                        created=job.created,
                        started=job.started,
                        finished=job.finished,
                        progress=job.progress,
                        links=job.links,
                    )

                    response = requests.get(
                        f"{self.settings.EMS_API_URL}/dags/{job.process_id}/dagRuns/{job.job_id}",
                        auth=self.ems_api_auth,
                    )
                    response.raise_for_status()

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

                    return crud.update_job(self.db, job.job_id, job.model_dump(by_alias=True))

        except LockError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to acquire lock. Please try again later.",
            )
        except requests.exceptions.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch DAG run {job.job_id} for DAG {job.process_id}: {e}",
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
