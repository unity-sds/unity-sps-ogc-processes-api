import uuid
from datetime import datetime

import requests
from fastapi import HTTPException, status
from redis.exceptions import LockError
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session

from openapi_server.config.config import Settings
from openapi_server.database import crud
from openapi_server.impl.dru_api import check_process_integrity
from openapi_server.utils.redis import RedisLock
from unity_sps_ogc_processes_api.apis.processes_api_base import BaseProcessesApi
from unity_sps_ogc_processes_api.models.execute200_response import Execute200Response
from unity_sps_ogc_processes_api.models.execute_workflows import ExecuteWorkflows
from unity_sps_ogc_processes_api.models.input_description import InputDescription
from unity_sps_ogc_processes_api.models.link import Link
from unity_sps_ogc_processes_api.models.metadata import Metadata
from unity_sps_ogc_processes_api.models.output_description import OutputDescription
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
        lock_key = f"process:{processId}"
        try:
            with self.redis_locking_client.lock(lock_key):
                process = crud.get_process(self.db, processId)

                # Convert metadata, links, inputs, and outputs if they exist
                metadata = (
                    [Metadata.model_validate(m) for m in process.metadata]
                    if process.metadata
                    else None
                )
                links = (
                    [Link.model_validate(link) for link in process.links]
                    if process.links
                    else None
                )
                inputs = (
                    {
                        k: InputDescription.model_validate(v)
                        for k, v in process.inputs.items()
                    }
                    if process.inputs
                    else None
                )
                outputs = (
                    {
                        k: OutputDescription.model_validate(v)
                        for k, v in process.outputs.items()
                    }
                    if process.outputs
                    else None
                )

                return Process(
                    title=process.title,
                    description=process.description,
                    keywords=process.keywords,
                    metadata=metadata,
                    id=process.id,
                    version=process.version,
                    job_control_options=process.job_control_options,
                    links=links,
                    inputs=inputs,
                    outputs=outputs,
                )
        except LockError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to acquire lock. Please try again later.",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def get_processes(self) -> ProcessList:
        processes = crud.get_processes(self.db)
        return ProcessList(
            processes=[
                ProcessSummary(
                    id=process.id,
                    title=process.title,
                    description=process.description,
                    keywords=process.keywords,
                    metadata=process.metadata,
                    version=process.version,
                    job_control_options=process.job_control_options,
                    links=process.links,
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
        lock_key = f"process:{processId}"
        try:
            with self.redis_locking_client.lock(lock_key):
                check_process_integrity(self.db, processId, new_process=False)

                # TODO
                # Fetch process description
                # Validate each execution input's value against the input schema in the process description
                # If there is a way to fetch the Airflow DAG inputs, also validate against that.
                # process_description = self.get_process_description(processId)

                # validated_inputs = {}
                # for input_id, input_value in execute_workflows.inputs.items():
                #     input_description = next(
                #         (input for input in process_description.inputs if input.id == input_id),
                #         None,
                #     )
                #     if input_description is None:
                #         raise HTTPException(
                #             status_code=status.HTTP_400_BAD_REQUEST,
                #             detail=f"Invalid input: {input_id}",
                #         )
                #     try:
                #         #validate(instance=input_value.value, schema=input_description.schema_)
                #         validated_inputs[input_id] = input_value.value
                #     except ValidationError as e:
                #         raise HTTPException(
                #             status_code=status.HTTP_400_BAD_REQUEST,
                #             detail=f"Invalid input for {input_id}: {e.message}",
                #         )
                #     validated_inputs[input_id] = input_value.value

                job_id = str(uuid.uuid4())
                logical_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

                inputs_dict = {}
                if execute_workflows.inputs:
                    for key, value in execute_workflows.inputs.items():
                        try:
                            inputs_dict[key] = value.model_dump(exclude_unset=True)
                        except Exception:
                            inputs_dict[key] = value

                data = {
                    "dag_run_id": job_id,
                    "logical_date": logical_date,
                    "conf": inputs_dict,
                }

                airflow_response = requests.post(
                    f"{self.settings.EMS_API_URL}/dags/{processId}/dagRuns",
                    json=data,
                    auth=self.ems_api_auth,
                )
                airflow_response.raise_for_status()

                job = StatusInfo(
                    processID=processId,
                    type="process",
                    jobID=job_id,
                    status=StatusCode.ACCEPTED,
                    created=datetime.now(),
                    updated=datetime.now(),
                )
                crud.create_job(self.db, job.model_dump(by_alias=True))
                if prefer == "respond-async":
                    # Asynchronous execution
                    return job
                else:
                    # Synchronous execution
                    # Note: In a real-world scenario, you'd wait for the job to complete
                    # and return the actual results. This is a simplified version.
                    # TODO get result from job using the result endpoint and return it here.
                    return Execute200Response(
                        {"result": "Sample output for synchronous execution"}
                    )

        except LockError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to acquire lock. Please try again later.",
            )
        except requests.exceptions.RequestException as e:
            status_code_to_raise = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail_message = (
                f"Failed to start DAG run {job_id} with DAG {processId}: {str(e)}"
            )

            if hasattr(e, "response"):
                detail_message = f"Failed to start DAG run {job_id} with DAG {processId}: {e.response.status_code} {e.response.reason}"

            raise HTTPException(status_code=status_code_to_raise, detail=detail_message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
