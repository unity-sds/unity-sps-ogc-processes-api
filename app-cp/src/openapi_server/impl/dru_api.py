import os
import shutil
import time

import requests
from fastapi import HTTPException, Response, status
from redis.exceptions import LockError
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from openapi_server.config.config import Settings
from openapi_server.database import crud
from openapi_server.utils.redis import RedisLock
from unity_sps_ogc_processes_api.apis.dru_api_base import BaseDRUApi
from unity_sps_ogc_processes_api.models.ogcapppkg import Ogcapppkg


def check_process_integrity(db: Session, process_id: str, new_process: bool):
    process = None
    try:
        process = crud.get_process(db, process_id)
        if new_process:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Process with ID '{process_id}' already exists",
            )
        # TODO: Check if deployment_status is complete
        # If not, raise an exception that its deployment status is not complete
    except NoResultFound:
        if not new_process:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Process with ID '{process_id}' not found",
            )
    except MultipleResultsFound:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Multiple processes found with same ID '{process_id}', data integrity error",
        )
    return process


class DRUApiImpl(BaseDRUApi):
    def __init__(
        self, settings: Settings, redis_locking_client: RedisLock, db: Session
    ):
        self.settings = settings
        self.redis_locking_client = redis_locking_client
        self.db = db

    def deploy(self, ogcapppkg: Ogcapppkg, w: str) -> Response:
        lock_key = f"process:{ogcapppkg.process_description.id}"
        try:
            with self.redis_locking_client.lock(lock_key, timeout=60):
                check_process_integrity(
                    self.db, ogcapppkg.process_description.id, new_process=True
                )
                # ogcapppkg.process_description.deployment_status = "deploying"
                crud.create_process(self.db, ogcapppkg)

                dag_filename = ogcapppkg.process_description.id + ".py"
                dag_catalog_filepath = os.path.join(
                    self.settings.DAG_CATALOG_DIRECTORY, dag_filename
                )
                if not os.path.isfile(dag_catalog_filepath):
                    existing_files = os.listdir(self.settings.DAG_CATALOG_DIRECTORY)
                    existing_files_str = "\n".join(existing_files)
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"The process ID '{ogcapppkg.process_description.id}' does not have a matching DAG file named '{dag_filename}' in the DAG catalog.\nThe DAG catalog includes the following files:\n{existing_files_str}",
                    )

                if os.path.isfile(
                    os.path.join(self.settings.DEPLOYED_DAGS_DIRECTORY, dag_filename)
                ):
                    # Log warning that file already exists in the deployed dags directory
                    pass

                shutil.copy2(
                    dag_catalog_filepath,
                    self.settings.DEPLOYED_DAGS_DIRECTORY,
                )

                if not os.path.isfile(
                    os.path.join(self.settings.DEPLOYED_DAGS_DIRECTORY, dag_filename)
                ):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Failed to copy DAG file to deployed directory",
                    )

                ems_api_auth = HTTPBasicAuth(
                    self.settings.EMS_API_AUTH_USERNAME,
                    self.settings.EMS_API_AUTH_PASSWORD.get_secret_value(),
                )
                timeout = 20
                start_time = time.time()
                while time.time() - start_time < timeout:
                    response = requests.get(
                        f"{self.settings.EMS_API_URL}/dags/{ogcapppkg.process_description.id}",
                        auth=ems_api_auth,
                    )
                    data = response.json()
                    if response.status_code == 404:
                        pass
                    elif data["is_paused"]:
                        self.pause_dag(
                            self.settings.EMS_API_URL,
                            ogcapppkg.process_description.id,
                            ems_api_auth,
                            pause=False,
                        )
                    elif data["is_active"]:
                        break
                    time.sleep(0.5)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                        detail=f"Timeout waiting for DAG '{ogcapppkg.process_description.id}' to be available in Airflow.",
                    )

                crud.update_process(
                    self.db,
                    ogcapppkg.process_description.id,
                    {"deployment_status": "deployed"},
                )

            return Response(
                status_code=status.HTTP_201_CREATED,
                content=f"Process {ogcapppkg.process_description.id} deployed successfully",
            )
        except LockError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to acquire lock. Please try again later.",
            )
        except HTTPException:
            # Re-raise HTTPExceptions without wrapping them
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def replace(self, processId: str, ogcapppkg: Ogcapppkg) -> None:
        lock_key = f"process:{processId}"
        try:
            with self.redis_locking_client.lock(lock_key, timeout=60):
                check_process_integrity(self.db, processId, new_process=False)
                # Validate the new ogcapppkg
                if ogcapppkg.process_description.id != processId:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Process ID in the path does not match the ID in the request body",
                    )

                # Update the existing process with new data
                crud.update_process(
                    self.db, processId, ogcapppkg.process_description.model_dump()
                )

                # Update the DAG file
                dag_filename = f"{processId}.py"
                dag_catalog_filepath = os.path.join(
                    self.settings.DAG_CATALOG_DIRECTORY, dag_filename
                )
                deployed_dag_path = os.path.join(
                    self.settings.DEPLOYED_DAGS_DIRECTORY, dag_filename
                )

                if os.path.exists(dag_catalog_filepath):
                    shutil.copy2(dag_catalog_filepath, deployed_dag_path)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"DAG file for process {processId} not found in the catalog",
                    )

                # Optionally, you might want to refresh the DAG in Airflow
                ems_api_auth = HTTPBasicAuth(
                    self.settings.EMS_API_AUTH_USERNAME,
                    self.settings.EMS_API_AUTH_PASSWORD.get_secret_value(),
                )
                response = requests.post(
                    f"{self.settings.EMS_API_URL}/dags/{processId}/dagRuns",
                    auth=ems_api_auth,
                    json={"is_paused": False},  # Unpause the DAG if it was paused
                )
                response.raise_for_status()

            return Response(
                status_code=status.HTTP_204_NO_CONTENT,
                content=f"Process {processId} replaced successfully",
            )
        except LockError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to acquire lock. Please try again later.",
            )
        except HTTPException:
            # Re-raise HTTPExceptions without wrapping them
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def undeploy(self, processId: str) -> None:
        lock_key = f"process:{processId}"
        try:
            with self.redis_locking_client.lock(lock_key, timeout=60):
                check_process_integrity(self.db, processId, new_process=False)

                ems_api_auth = HTTPBasicAuth(
                    self.settings.EMS_API_AUTH_USERNAME,
                    self.settings.EMS_API_AUTH_PASSWORD.get_secret_value(),
                )

                # Pause the DAG first
                self.pause_dag(
                    self.settings.EMS_API_URL, processId, ems_api_auth, pause=True
                )

                # List and stop active DAG runs
                active_dag_runs = self.list_active_dag_runs(
                    self.settings.EMS_API_URL, processId, ems_api_auth
                )
                for dag_run in active_dag_runs:
                    self.stop_dag_run(
                        self.settings.EMS_API_URL,
                        processId,
                        dag_run["dag_run_id"],
                        ems_api_auth,
                    )
                    self.stop_task_instances(
                        self.settings.EMS_API_URL,
                        processId,
                        dag_run["dag_run_id"],
                        ems_api_auth,
                    )

                # Remove the DAG file from the deployed directory
                dag_filename = f"{processId}.py"
                deployed_dag_path = os.path.join(
                    self.settings.DEPLOYED_DAGS_DIRECTORY, dag_filename
                )
                if os.path.isfile(deployed_dag_path):
                    try:
                        os.remove(deployed_dag_path)
                    except OSError as e:
                        raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to remove DAG file from deployed DAGs directory: {e.strerror}",
                        )

                # Poll for the removal of the DAG from the Airflow API
                timeout = 20
                start_time = time.time()
                while time.time() - start_time < timeout:
                    response = requests.get(
                        f"{self.settings.EMS_API_URL}/dags/{processId}",
                        auth=ems_api_auth,
                    )
                    data = response.json()
                    if response.status_code == 404:
                        break
                    elif not data["is_active"]:
                        break
                    time.sleep(0.5)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                        detail="Timeout waiting for DAG to be fully removed from Airflow.",
                    )

                # Delete the process from the database
                crud.delete_process(self.db, processId)

            return Response(
                status_code=status.HTTP_204_NO_CONTENT,
                content=f"Process {processId} undeployed successfully",
            )
        except LockError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to acquire lock. Please try again later.",
            )
        except HTTPException:
            # Re-raise HTTPExceptions without wrapping them
            raise
        except Exception as e:
            # For any other exception, wrap it in a generic HTTPException
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def pause_dag(self, airflow_url, dag_id, auth, pause=True):
        endpoint = f"{airflow_url}/dags/{dag_id}"
        data = {"is_paused": pause}
        response = requests.patch(endpoint, auth=auth, json=data)
        response.raise_for_status()

    def list_active_dag_runs(self, airflow_url, dag_id, auth):
        endpoint = f"{airflow_url}/dags/{dag_id}/dagRuns"
        params = {"state": "running"}
        response = requests.get(endpoint, auth=auth, params=params)
        response.raise_for_status()
        return response.json()["dag_runs"]

    def stop_dag_run(self, airflow_url, dag_id, dag_run_id, auth):
        endpoint = f"{airflow_url}/dags/{dag_id}/dagRuns/{dag_run_id}"
        data = {"state": "failed"}
        response = requests.patch(endpoint, auth=auth, json=data)
        response.raise_for_status()

    def stop_task_instances(self, airflow_url, dag_id, dag_run_id, auth):
        endpoint = f"{airflow_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances"
        tasks = requests.get(endpoint, auth=auth)
        tasks.raise_for_status()

        for task in tasks.json()["task_instances"]:
            task_instance_endpoint = f"{airflow_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task['task_id']}"
            update_data = {"dry_run": False, "new_state": "failed"}
            update_response = requests.patch(
                task_instance_endpoint, auth=auth, json=update_data
            )
            update_response.raise_for_status()
