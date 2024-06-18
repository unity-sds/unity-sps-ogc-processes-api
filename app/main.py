# generated by fastapi-codegen:
#   filename:  ogcapi-processes.yaml
#   timestamp: 2024-02-16T19:06:21+00:00

from __future__ import annotations

import os
import shutil
import time
import uuid
from datetime import datetime
from functools import lru_cache

import requests
from fastapi import BackgroundTasks, Body, Depends, FastAPI, HTTPException
from fastapi import status as fastapi_status
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from typing_extensions import Annotated

from . import config, cwl_arbitrary_dag
from .database import SessionLocal, crud, engine, models
from .redis import RedisLock
from .schemas.ogc_processes import (
    ConfClasses,
    Execute,
    JobList,
    LandingPage,
    Link,
    Process,
    ProcessList,
    ProcessSummary,
    Results,
    StatusCode,
    StatusInfo,
    Type2,
)
from .schemas.unity_sps import HealthCheck

models.Base.metadata.create_all(bind=engine)  # Create database tables


app = FastAPI(
    version="1.0.0",
    title="Unity Processing API conforming to the OGC API - Processes - Part 1 standard",
    description="This document is an API definition document provided alongside the OGC API - Processes standard. The OGC API - Processes Standard specifies a processing interface to communicate over a RESTful protocol using JavaScript Object Notation (JSON) encodings. The specification allows for the wrapping of computational tasks into executable processes that can be offered by a server and be invoked by a client application.",
    # contact={"name": "Placeholder", "email": "Placeholder"},
    license={"name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
    servers=[],
)


@lru_cache
def get_settings():
    return config.Settings()


@lru_cache()
def get_redis_locking_client():
    settings = get_settings()
    return RedisLock(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


# @lru_cache()
# def get_ems_client():
#     settings = get_settings()
#     configuration = Configuration(
#         host=settings.EMS_API_URL,
#         username=settings.EMS_API_AUTH_USERNAME,
#         password=settings.EMS_API_AUTH_PASSWORD.get_secret_value(),
#     )
#     return ApiClient(configuration)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_process_integrity(db: Session, process_id: str, new_process: bool):
    process = None
    try:
        process = crud.get_process(db, process_id)
        # TODO If not a new process, check if deployment_status is complete
        # If not, raise an exception that it it's deployment status is not complete
        if new_process and process is not None:
            raise ValueError
    except NoResultFound:
        if not new_process:
            raise HTTPException(
                status_code=fastapi_status.HTTP_404_NOT_FOUND,
                detail=f"Process with ID '{process_id}' not found",
            )
    except MultipleResultsFound:
        raise HTTPException(
            status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Multiple processes found with same ID '{process_id}', data integrity error",
        )
    except ValueError:
        raise HTTPException(
            status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Existing process with ID '{process_id}' already exists",
        )
    return process


def check_job_integrity(db: Session, job_id: str, new_job: bool):
    job = None
    try:
        job = crud.get_job(db, job_id)
        if new_job and job is not None:
            raise ValueError
    except NoResultFound:
        if not new_job:
            raise HTTPException(
                status_code=fastapi_status.HTTP_404_NOT_FOUND, detail=f"Job with ID '{job_id}' not found"
            )
    except MultipleResultsFound:
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


@app.get("/", response_model=LandingPage, summary="Landing page of this API")
async def landing_page():
    """
    The landing page provides links to the:
    - API Definition (no fixed path),
    - Conformance Statements (`/conformance`),
    - Processes Metadata (`/processes`),
    - Endpoint for Job Monitoring (`/jobs`).

    For more information, see [Section 7.2](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_landing_page).
    """
    return LandingPage(
        title="Unity SPS Processing Server",
        description="Server implementing the OGC API - Processes 1.0 Standard",
        links=[Link(href="/conformance"), Link(href="/processes"), Link(href="/jobs")],
    )


@app.get(
    "/health",
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=fastapi_status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


@app.get(
    "/conformance",
    response_model=ConfClasses,
    summary="Information about standards that this API conforms to",
)
async def conformance_declaration():
    """
    A list of all conformance classes, specified in a standard, that the server conforms to.

    | Conformance class | URI |
    | -------- | ------- |
    | Core | http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/core |
    | OGC Process Description | http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/ogc-process-description |
    | JSON | http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/json |
    | HTML | http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/html |
    | OpenAPI | Specification 3.0	http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/oas30 |
    | Job list | http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/job-list |
    | Callback | http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/callback |
    | Dismiss |	http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/dismiss |

    For more information, see [Section 7.4](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_conformance_classes).
    """
    return ConfClasses(
        conformsTo=["http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/ogc-process-description"]
    )


def pause_dag(airflow_url, dag_id, auth, pause=True):
    """Pauses or unpauses a DAG based on the pause parameter."""
    endpoint = f"{airflow_url}/dags/{dag_id}"
    data = {"is_paused": pause}
    response = requests.patch(endpoint, auth=auth, json=data)
    response.raise_for_status()


def list_active_dag_runs(airflow_url, dag_id, auth):
    """Fetches all active DAG runs for a specific DAG."""
    endpoint = f"{airflow_url}/dags/{dag_id}/dagRuns"
    params = {"state": "running"}  # Adjust the states as necessary
    response = requests.get(endpoint, auth=auth, params=params)
    response.raise_for_status()
    return response.json()["dag_runs"]


def stop_dag_run(airflow_url, dag_id, dag_run_id, auth):
    """Stops a specific DAG run by updating its state to 'failed'."""
    endpoint = f"{airflow_url}/dags/{dag_id}/dagRuns/{dag_run_id}"
    data = {"state": "failed"}  # Use 'failed' or another terminal state
    response = requests.patch(endpoint, auth=auth, json=data)
    response.raise_for_status()


def stop_task_instances(airflow_url, dag_id, dag_run_id, auth):
    """Stops all task instances of a specific DAG run."""
    endpoint = f"{airflow_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances"
    tasks = requests.get(endpoint, auth=auth)
    tasks.raise_for_status()

    for task in tasks.json()["task_instances"]:
        task_instance_endpoint = (
            f"{airflow_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task['task_id']}"
        )
        update_data = {"dry_run": False, "new_state": "failed"}
        update_response = requests.patch(task_instance_endpoint, auth=auth, json=update_data)
        update_response.raise_for_status()


# def deploy_process_background(
#     settings: config.Settings,
#     db: Session,
#     process: Process,
# ):
#     lock_id = f"process_deploy_{process.id}"
#     try:
#         with redis_lock.lock(lock_id, timeout=20):
#             check_process_integrity(db, process.id, new_process=True)
#             # Add the actual deployment logic here
#             # For example, file copying, Airflow DAG interaction, etc.
#             crud.create_process(db, process)
#     except LockError as e:
#         raise HTTPException(status_code=409, detail=str(e))


# @app.post("/processes", response_model=Process, summary="Deploy a process")
# def deploy_process(
#     background_tasks: BackgroundTasks,
#     settings: Annotated[config.Settings, Depends(get_settings)],
#     db: Session = Depends(get_db),
#     process: Process = Body(...),
# ):
#     background_tasks.add_task(deploy_process_background, settings, db, process)
#     return {"message": "Process deployment initiated."}


@app.post("/processes", response_model=Process, summary="Deploy a process")
def deploy_process(
    background_tasks: BackgroundTasks,
    settings: Annotated[config.Settings, Depends(get_settings)],
    redis_locking_client: Annotated[RedisLock, Depends(get_redis_locking_client)],
    db: Session = Depends(get_db),
    process: Process = Body(...),
):
    """
    Deploy a new process.

    **Note:** This is not an officially supported endpoint in the OGC Processes specification.
    """
    check_process_integrity(db, process.id, new_process=True)

    with redis_locking_client.lock("deploy_process_" + process.id):  # as lock:
        pass

    # Acquire lock
    # Create process in DB w/ deployment_status field "deploying"
    # Check if DAG exists in Airflow
    # Check if file exists in DAG folder
    # Check if file exists in DAG catalog
    # Copy file to DAG folder
    # Poll Airflow until DAG appears
    # Unpause DAG
    # Check if DAG is_active is True
    # Update process in DB w/ deployment_status field "deployed"
    # Release lock

    # Verify that the process_id corresponds with a DAG ID by filename in the DAG catalog
    dag_filename = process.id + ".py"
    dag_catalog_filepath = os.path.join(settings.DAG_CATALOG_DIRECTORY, dag_filename)
    if not os.path.isfile(dag_catalog_filepath):
        if process.executionunit.type == "application/cwl":
            cwl_arbitrary_dag.write_dag(dag_catalog_filepath,process.id,process.executionunit.href,dict(),process.processdescription)
        else:
            # If the file doesn't exist and the executionunit wasn't provided,
            #     list other files in the same directory
            existing_files = os.listdir(settings.DAG_CATALOG_DIRECTORY)
            existing_files_str = "\n".join(existing_files)  # Create a string from the list of files

            # Raise an exception with details about what files are actually there
            raise HTTPException(
                status_code=fastapi_status.HTTP_409_CONFLICT,
                detail=f"The process ID '{process.id}' does not have a matching DAG file named '{dag_filename}' in the DAG catalog.\nThe DAG catalog includes the following files:\n{existing_files_str}",
            )

    if os.path.isfile(os.path.join(settings.DEPLOYED_DAGS_DIRECTORY, dag_filename)):
        # Log warning that file already exists in the deployed dags directory
        pass

    # Copy DAG from the DAG catalog PVC to deployed PVC
    shutil.copy2(
        dag_catalog_filepath,
        settings.DEPLOYED_DAGS_DIRECTORY,
    )

    if not os.path.isfile(os.path.join(settings.DEPLOYED_DAGS_DIRECTORY, dag_filename)):
        raise HTTPException(
            status_code=fastapi_status.HTTP_409_CONFLICT,
            detail="",
        )

    # Poll the EMS API to verify DAG existence
    ems_api_auth = HTTPBasicAuth(
        settings.EMS_API_AUTH_USERNAME, settings.EMS_API_AUTH_PASSWORD.get_secret_value()
    )
    timeout = 20
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = requests.get(f"{settings.EMS_API_URL}/dags/{process.id}", auth=ems_api_auth)
        data = response.json()
        if response.status_code == 404:
            pass
        elif data["is_paused"]:
            pause_dag(settings.EMS_API_URL, process.id, ems_api_auth, pause=False)
        elif data["is_active"]:
            break
        time.sleep(0.5)
    else:
        raise HTTPException(
            status_code=fastapi_status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Timeout waiting for DAG '{process.id}' to be available in Airflow.",
        )

    return crud.create_process(db, process)


@app.delete(
    "/processes/{process_id}", status_code=fastapi_status.HTTP_204_NO_CONTENT, summary="Undeploy a process"
)
def undeploy_process(
    background_tasks: BackgroundTasks,
    settings: Annotated[config.Settings, Depends(get_settings)],
    redis_locking_client: Annotated[RedisLock, Depends(get_redis_locking_client)],
    process_id: str,
    db: Session = Depends(get_db),
    force: bool = False,
):
    """
    Undeploy an existing process.

    **Note:** This is not an officially supported endpoint in the OGC Processes specification.
    """
    process = check_process_integrity(db, process_id, new_process=False)

    with redis_locking_client.lock("deploy_process_" + process.id):  # as lock:
        pass

    # Acquire lock
    # Update process in DB w/ deployment_status field "undeploying"
    # Check if DAG exists in Airflow
    # Pause the DAG
    # Stop all DAG runs and tasks
    # Remove file from dag folder
    # Ensure DAG field is_active turns to False
    # Delete process from DB
    # Release lock

    ems_api_auth = HTTPBasicAuth(
        settings.EMS_API_AUTH_USERNAME, settings.EMS_API_AUTH_PASSWORD.get_secret_value()
    )
    # response = requests.get(f"{settings.EMS_API_URL}/dags/{process_id}", auth=ems_api_auth)
    # if response.status_code == 200:
    #     return True  # DAG exists
    # elif response.status_code == 404:
    #     return False  # DAG does not exist
    # else:
    #     response.raise_for_status()  # Raise an exception for other HTTP errors

    active_dag_runs = list_active_dag_runs(settings.EMS_API_URL, process_id, ems_api_auth)
    if len(active_dag_runs) and not force:
        raise HTTPException(
            status_code=fastapi_status.HTTP_409_CONFLICT,
            detail="Process has active DAG runs. Set 'force' to true to override and stop all active DAG runs and tasks.",
        )

    # Pause the DAG first
    pause_dag(settings.EMS_API_URL, process_id, ems_api_auth, pause=True)

    for dag_run in active_dag_runs:
        stop_dag_run(settings.EMS_API_URL, process_id, dag_run["dag_run_id"], ems_api_auth)
        stop_task_instances(settings.EMS_API_URL, process_id, dag_run["dag_run_id"], ems_api_auth)

    dag_filename = process_id + ".py"
    deployed_dag_filepath = os.path.join(settings.DEPLOYED_DAGS_DIRECTORY, dag_filename)
    if os.path.isfile(deployed_dag_filepath):
        try:
            os.remove(deployed_dag_filepath)
        except OSError as e:
            raise HTTPException(
                status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to remove DAG file from deployed DAGs directory: {e.strerror}",
            )

    # Poll for the removal of the DAG from the Airflow API
    timeout = 20
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = requests.get(f"{settings.EMS_API_URL}/dags/{process_id}", auth=ems_api_auth)
        data = response.json()
        if response.status_code == 404:
            break
        elif not data["is_active"]:
            break
        time.sleep(0.5)
    else:
        raise HTTPException(
            status_code=fastapi_status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Timeout waiting for DAG to be fully removed from Airflow.",
        )

    crud.delete_process(db, process)


@app.get("/processes", response_model=ProcessList, summary="Retrieve the list of available processes")
def process_list(db: Session = Depends(get_db)):
    """
    The list of processes contains a summary of each process the OGC API - Processes offers, including the link to a more detailed description of the process.

    For more information, see [Section 7.9](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_process_list).
    """
    processes = crud.get_processes(db)
    process_summaries = []
    for p in processes:
        process_summaries.append(ProcessSummary(**Process.model_validate(p).model_dump()))
    links = [
        Link(href="/processes", rel="self", type="application/json", hreflang=None, title="List of processes")
    ]
    return ProcessList(processes=process_summaries, links=links)


@app.get("/processes/{process_id}", response_model=Process, summary="Retrieve a process description")
def process_description(process_id: str, db: Session = Depends(get_db)):
    """
    The process description contains information about inputs and outputs and a link to the execution-endpoint for the process. The Core does not mandate the use of a specific process description to specify the interface of a process. That said, the Core requirements class makes the following recommendation:

    Implementations SHOULD consider supporting the OGC process description.

    For more information, see [Section 7.10](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_process_description).
    """
    return check_process_integrity(db, process_id, new_process=False)


@app.get("/jobs", response_model=JobList, summary="Retrieve the list of jobs")
def job_list(db: Session = Depends(get_db)):
    """
    Lists available jobs.

    For more information, see [Section 11](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_job_list).
    """
    jobs = crud.get_jobs(db)
    links = [Link(href="/jobs", rel="self", type="application/json", hreflang=None, title="List of jobs")]
    return JobList(jobs=jobs, links=links)


@app.post("/processes/{process_id}/execution", response_model=StatusInfo, summary="Execute a process")
def execute(
    settings: Annotated[config.Settings, Depends(get_settings)],
    process_id: str,
    execute: Execute = Body(...),
    db: Session = Depends(get_db),
):
    """
    Create a new job.

    For more information, see [Section 7.11](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_create_job).
    """
    check_process_integrity(db, process_id, new_process=False)
    ems_api_auth = HTTPBasicAuth(
        settings.EMS_API_AUTH_USERNAME, settings.EMS_API_AUTH_PASSWORD.get_secret_value()
    )
    try:
        response = requests.get(f"{settings.EMS_API_URL}/dags/{process_id}", auth=ems_api_auth)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        status_code_to_raise = fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR
        detail_message = f"Failed to fetch DAG {process_id} due to an error."
        if hasattr(e, "response"):
            # If the exception has a response attribute, it's likely an HTTPError with more info
            detail_message = f"Failed to fetch DAG {process_id}: {e.response.status_code} {e.response.reason}"

        raise HTTPException(status_code=status_code_to_raise, detail=detail_message)

    # TODO Validate that that the inputs and outputs conform to the schemas for inputs and outputs of the process
    job_id = str(uuid.uuid4())
    logical_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    data = {"dag_run_id": job_id, "logical_date": logical_date, "conf": {**execute.model_dump()}}
    try:
        response = requests.post(
            f"{settings.EMS_API_URL}/dags/{process_id}/dagRuns", json=data, auth=ems_api_auth
        )
        response.raise_for_status()
        check_job_integrity(db, job_id, new_job=True)
        job = StatusInfo(
            jobID=job_id,
            processID=process_id,
            type=Type2.process.value,
            status=StatusCode.accepted.value,
        )
        return crud.create_job(db, execute, job)
    except requests.exceptions.RequestException as e:
        status_code_to_raise = fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR
        detail_message = f"Failed to start DAG run {job_id} with DAG {process_id} due to an error."

        if hasattr(e, "response"):
            # If the exception has a response attribute, it's likely an HTTPError with more info
            detail_message = f"Failed to start a DAG run {job_id} with DAG {process_id}: {e.response.status_code} {e.response.reason}"

        raise HTTPException(status_code=status_code_to_raise, detail=detail_message)


@app.get("/jobs/{job_id}", response_model=StatusInfo, summary="Retrieve the status of a job")
def status(
    settings: Annotated[config.Settings, Depends(get_settings)], job_id: str, db: Session = Depends(get_db)
):
    """
    Shows the status of a job.

    For more information, see [Section 7.12](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_retrieve_status_info).
    """
    job = check_job_integrity(db, job_id, new_job=False)
    job = StatusInfo.model_validate(job)
    ems_api_auth = HTTPBasicAuth(
        settings.EMS_API_AUTH_USERNAME, settings.EMS_API_AUTH_PASSWORD.get_secret_value()
    )
    try:
        response = requests.get(
            f"{settings.EMS_API_URL}/dags/{job.processID}/dagRuns/{job.jobID}",
            auth=ems_api_auth,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        status_code_to_raise = fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR
        detail_message = f"Failed to fetch DAG run {job.jobID} for DAG {job.processID} due to an error."
        if hasattr(e, "response"):
            # If the exception has a response attribute, it's likely an HTTPError with more info
            detail_message = f"Failed to fetch DAG run {job.jobID} for DAG {job.processID}: {e.response.status_code} {e.response.reason}"

        raise HTTPException(status_code=status_code_to_raise, detail=detail_message)

    execution_status_conversion_dict = {
        "queued": StatusCode.accepted,
        "running": StatusCode.running,
        "success": StatusCode.successful,
        "failed": StatusCode.failed,
    }
    data = response.json()
    current_execution_status = execution_status_conversion_dict[data["state"]].value
    if job.status != current_execution_status:
        job.status = current_execution_status
        updated = datetime.now()
        job.updated = updated

    end_date_str = data.get("end_date", None)
    if end_date_str:
        end_date = datetime.fromisoformat(end_date_str)
        job.finished = end_date

    return crud.update_job(db, job)


@app.delete(
    "/jobs/{job_id}", response_model=StatusInfo, summary="Cancel a job execution, remove a finished job"
)
def dismiss(
    settings: Annotated[config.Settings, Depends(get_settings)], job_id: str, db: Session = Depends(get_db)
):
    """
    Cancel a job execution and remove it from the jobs list.

    For more information, see [Section 13](https://docs.ogc.org/is/18-062r2/18-062r2.html#Dismiss).
    """
    job = check_job_integrity(db, job_id, new_job=False)
    ems_api_auth = HTTPBasicAuth(
        settings.EMS_API_AUTH_USERNAME, settings.EMS_API_AUTH_PASSWORD.get_secret_value()
    )
    try:
        # TODO also need to cancel all task instances
        response = requests.delete(
            f"{settings.EMS_API_URL}/dags/{job.processID}/dagRuns/{job.jobID}",
            auth=ems_api_auth,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        status_code_to_raise = fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR
        detail_message = f"Failed to fetch DAG run {job.jobID} for DAG {job.processID} due to an error."
        if hasattr(e, "response"):
            # If the exception has a response attribute, it's likely an HTTPError with more info
            detail_message = f"Failed to fetch DAG run {job.jobID} for DAG {job.processID}: {e.response.status_code} {e.response.reason}"

        raise HTTPException(status_code=status_code_to_raise, detail=detail_message)

    crud.delete_job(db, job)
    job.status = StatusCode.dismissed.value
    return job


@app.get("/jobs/{job_id}/results", response_model=Results, summary="Retrieve the result(s) of a job")
def results(job_id: str, db: Session = Depends(get_db)):
    """
    Lists available results of a job. In case of a failure, lists exceptions instead.

    For more information, see [Section 7.13](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_retrieve_job_results).
    """
    check_job_integrity(db, job_id, new_job=False)
    return crud.get_results(db, job_id)
