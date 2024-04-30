from fastapi.testclient import TestClient
import uuid

from .main import app
from .schemas.ogc_processes import (
    ConfClasses,
    LandingPage,
    Process,
    ProcessList,
    StatusInfo,
    JobList,
    Results,
    StatusCode,
    Execute
)


client = TestClient(app)


def test_get_landing_page():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    landing_page = LandingPage.model_validate(data)
    assert landing_page.title == "Unity SPS Processing Server"


def test_get_conformance_declaration():
    response = client.get("/conformance")
    assert response.status_code == 200
    data = response.json()
    conformance_declaration = ConfClasses.model_validate(data)
    assert len(conformance_declaration.conformsTo) > 0
    assert conformance_declaration.conformsTo == [
        "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/ogc-process-description"
    ]


def test_deploy_process():
    process = Process(
        id="test",
        version="1.0",
        jobcontroloptions=["async-execute", "sync-execute"],
        links=[{"href": "http://example.com", "rel": "self"}],
        inputs=[{"input1": "data1"}],
        outputs=[{"output1": "result1"}],
    )
    response = client.post("/processes", json=process.model_dump())
    assert response.status_code == 200
    data = response.json()
    process = Process.model_validate(data)
    assert process.id == "test"


def test_get_process_list():
    response = client.get("/processes")
    assert response.status_code == 200
    data = response.json()
    assert ProcessList.model_validate(data)


def test_get_process_description():
    process_id = "test"
    response = client.get(f"/processes/{process_id}")
    assert response.status_code == 200
    data = response.json()
    process = Process.model_validate(data)
    assert process.id == process_id


def test_get_job_list():
    response = client.get("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert JobList.model_validate(data)


# def test_post_execute():
#     process = Process(
#         id="test",
#         version="1.0",
#         jobcontroloptions=["async-execute", "sync-execute"],
#         links=[{"href": "http://example.com", "rel": "self"}],
#         inputs=[{"input1": "data1"}],
#         outputs=[{"output1": "result1"}],
#     )
#     response = client.post(f"/processes/{process.id}/execution", json=process.model_dump())
#     print(response)
#     assert response.status_code == 200
#     data = response.json()
#     process = Process.model_validate(data)
#     assert process.id == "test"


def test_get_status():
    job_id = uuid.uuid4()
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    status_info = StatusInfo.model_validate(data)
    assert status_info.jobID == job_id


def test_delete_dismiss():
    job_id = uuid.uuid4()
    response = client.delete(f"/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    status_info = StatusInfo.model_validate(data)
    assert status_info.status == StatusCode.dismissed


def test_get_results():
    job_id = uuid.uuid4()
    response = client.get(f"/jobs/{job_id}/results")
    assert response.status_code == 200
    data = response.json()
    assert Results.model_validate(data)
