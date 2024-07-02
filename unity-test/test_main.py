import json
import os

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


@pytest.mark.dependency()
def test_post_deploy_process(test_directory, client):
    data_filename = os.path.join(test_directory, "test_data/process_descriptions/EchoProcess.json")
    f = open(data_filename)
    process_json = json.load(f)
    process = Process.model_validate(process_json)
    response = client.post("/processes", json=process.model_dump())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    process = Process.model_validate(data)
    assert process.id == "EchoProcess"


@pytest.mark.dependency(depends=["test_post_deploy_process"])
def test_delete_undeploy_process(client):
    response = client.delete("/processes/EchoProcess")
    assert response.status_code == status.HTTP_409_CONFLICT
    response = client.delete("/processes/EchoProcess", params={"force": True})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_post_execute_process(test_directory, client, deploy_process):
    data_filename = os.path.join(test_directory, "test_data/execution_requests/execute_cwltool_help_dag.json")
    f = open(data_filename)
    execute_json = json.load(f)
    execute = Execute.model_validate(execute_json)
    response = client.post(f"/processes/{deploy_process.id}/execution", json=jsonable_encoder(execute))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert StatusInfo.model_validate(data)


def test_delete_dismiss_execution(test_directory, client, deploy_process):
    data_filename = os.path.join(test_directory, "test_data/execution_requests/execute_cwltool_help_dag.json")
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


@pytest.mark.dependency()
def test_post_deploy_process_cwl_dag(test_directory, client):
    data_filename = os.path.join(test_directory, "test_data/process_descriptions/cwl_dag_process.json")
    f = open(data_filename)
    process_json = json.load(f)
    process = Process.model_validate(process_json)
    response = client.post("/processes", json=process.model_dump())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    process = Process.model_validate(data)
    assert process.id == "cwl_dag"
    assert process.title == "CWL DAG Process"


@pytest.mark.dependency(depends=["test_post_deploy_process_cwl_dag"])
def test_post_execute_process_cwl_dag(test_directory, client):
    data_filename = os.path.join(test_directory, "test_data/execution_requests/cwl_dag_request.json")
    f = open(data_filename)
    execute_json = json.load(f)
    execute = Execute.model_validate(execute_json)
    response = client.post("/processes/cwl_dag/execution", json=jsonable_encoder(execute))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert StatusInfo.model_validate(data)
    assert data["processID"] == "cwl_dag"
    assert data["type"] == "process"


@pytest.mark.dependency(depends=["test_post_execute_process_cwl_dag"])
def test_get_status_cwl_dag(test_directory, client):
    data_filename = os.path.join(test_directory, "test_data/execution_requests/cwl_dag_request.json")
    f = open(data_filename)
    execute_json = json.load(f)
    execute = Execute.model_validate(execute_json)
    execute_response = client.post("/processes/cwl_dag/execution", json=jsonable_encoder(execute))
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


@pytest.mark.dependency(depends=["test_get_status_cwl_dag"])
def test_delete_undeploy_cwl_dag(client):
    response = client.delete("/processes/cwl_dag")
    assert response.status_code == status.HTTP_409_CONFLICT
    response = client.delete("/processes/cwl_dag", params={"force": True})
    assert response.status_code == status.HTTP_204_NO_CONTENT
