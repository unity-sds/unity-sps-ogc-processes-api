import glob
import json
import os
import pathlib

import pytest
from fastapi import status
from fastapi.encoders import jsonable_encoder

from app.schemas.ogc_processes import (
    ConfClasses,
    Execute,
    JobList,
    LandingPage,
    Process,
    ProcessList,
    Results,
    StatusCode,
    StatusInfo,
)
from app.schemas.unity_sps import HealthCheck

TEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")
PROCESS_FILES = glob.glob(f"{TEST_DIR}/process_descriptions/*.json")
EXECUTION_FILES = glob.glob(f"{TEST_DIR}/execution_requests/*.json")


def test_get_landing_page(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    landing_page = LandingPage.model_validate(data)
    assert landing_page.title == "Unity SPS Processing Server"


def test_get_health(client):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    landing_page = HealthCheck.model_validate(data)
    assert landing_page.status == "OK"


def test_get_conformance_declaration(client):
    response = client.get("/conformance")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    conformance_declaration = ConfClasses.model_validate(data)
    assert len(conformance_declaration.conformsTo) > 0
    assert conformance_declaration.conformsTo == [
        "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/ogc-process-description"
    ]


@pytest.mark.parametrize("process_filename", PROCESS_FILES)
@pytest.mark.dependency(name="test_post_deploy_process")
def test_post_deploy_process(client, process_filename):
    f = open(process_filename)
    process_json = json.load(f)
    process = Process.model_validate(process_json)
    response = client.post("/processes", json=process.model_dump())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    process = Process.model_validate(data)
    assert process.id == pathlib.Path(process_filename).stem


@pytest.mark.parametrize("process_filename", PROCESS_FILES)
@pytest.mark.dependency(depends=["test_post_deploy_process"])
def test_delete_undeploy_process(client, process_filename):
    process_id = pathlib.Path(process_filename).stem
    response = client.delete(f"/processes/{process_id}")
    assert response.status_code == status.HTTP_409_CONFLICT
    response = client.delete(f"/processes/{process_id}", params={"force": True})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_post_execute_process(test_directory, client, deploy_process):
    f = open(os.path.join(test_directory, f"test_data/execution_requests/{deploy_process.id}.json"))
    execute_json = json.load(f)
    execute = Execute.model_validate(execute_json)
    response = client.post(f"/processes/{deploy_process.id}/execution", json=jsonable_encoder(execute))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert StatusInfo.model_validate(data)


def test_delete_dismiss_execution(test_directory, client, deploy_process):
    data_filename = os.path.join(test_directory, f"test_data/execution_requests/{deploy_process.id}.json")
    f = open(data_filename)
    execute_json = json.load(f)
    execute = Execute.model_validate(execute_json)
    response = client.post(f"/processes/{deploy_process.id}/execution", json=jsonable_encoder(execute))
    data = response.json()
    status_info = StatusInfo.model_validate(data)

    response = client.delete(f"/jobs/{status_info.jobID}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    status_info = StatusInfo.model_validate(data)
    assert status_info.status == StatusCode.dismissed.value


def test_get_process_description(client, deploy_process):
    response = client.get(f"/processes/{deploy_process.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    process = Process.model_validate(data)
    assert process.id == deploy_process.id


def test_get_process_list(client):
    response = client.get("/processes")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert ProcessList.model_validate(data)


def test_get_job_list(client):
    response = client.get("/jobs")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert JobList.model_validate(data)


def test_get_status(client, execute_process):
    response = client.get(f"/jobs/{execute_process.jobID}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    status_info = StatusInfo.model_validate(data)
    assert status_info.jobID == execute_process.jobID


def test_get_results(client, execute_process):
    response = client.get(f"/jobs/{execute_process.jobID}/results")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert Results.model_validate(data)


@pytest.mark.parametrize("process_filename", PROCESS_FILES)
def test_post_deploy_process_dag(test_directory, client, process_filename):
    f = open(process_filename)
    process_json = json.load(f)
    process = Process.model_validate(process_json)
    response = client.post("/processes", json=process.model_dump())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    process = Process.model_validate(data)
    assert process.id == pathlib.Path(process_filename).stem


@pytest.mark.dependency(name="test_post_execute_process_dag")
@pytest.mark.parametrize("execution_filename", EXECUTION_FILES)
def test_post_execute_process_dag(test_directory, client, execution_filename):
    f = open(execution_filename)
    execute_json = json.load(f)
    execute = Execute.model_validate(execute_json)
    process_id = pathlib.Path(execution_filename).stem
    response = client.post(f"/processes/{process_id}/execution", json=jsonable_encoder(execute))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert StatusInfo.model_validate(data)
    assert data["processID"] == process_id
    assert data["type"] == "process"


@pytest.mark.parametrize("execution_filename", EXECUTION_FILES)
def test_get_status_dag(test_directory, client, execution_filename):
    f = open(execution_filename)
    execute_json = json.load(f)
    execute = Execute.model_validate(execute_json)
    process_id = pathlib.Path(execution_filename).stem
    execute_response = client.post(f"/processes/{process_id}/execution", json=jsonable_encoder(execute))
    data = execute_response.json()
    status_info = StatusInfo.model_validate(data)
    job_id = status_info.jobID

    code = status.HTTP_404_NOT_FOUND
    while code != status.HTTP_200_OK:
        status_response = client.get(f"/jobs/{job_id}")
        code = status_response.status_code

    assert status_response.status_code == status.HTTP_200_OK
    data = status_response.json()
    status_info = StatusInfo.model_validate(data)
    assert status_info.jobID == job_id


@pytest.mark.parametrize("process_filename", PROCESS_FILES)
@pytest.mark.dependency(depends=["test_post_execute_process_dag"])
def test_delete_undeploy_dag(client, process_filename):
    process_id = pathlib.Path(process_filename).stem
    response = client.delete(f"/processes/{process_id}")
    assert response.status_code == status.HTTP_409_CONFLICT
    response = client.delete(f"/processes/{process_id}", params={"force": True})
    assert response.status_code == status.HTTP_204_NO_CONTENT
