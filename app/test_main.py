from fastapi.testclient import TestClient

from .main import app
from .schemas.ogc_processes import ConfClasses, LandingPage, ProcessList, StatusInfo

client = TestClient(app)


def test_get_landing_page():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    landing_page = LandingPage(**data)
    assert landing_page.title == "Unity SPS Processing Server"


def test_get_conformance_declaration():
    response = client.get("/conformance")
    assert response.status_code == 200
    data = response.json()
    conformance_declaration = ConfClasses(**data)
    assert len(conformance_declaration.conformsTo) > 0
    assert conformance_declaration.conformsTo == [
        "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/ogc-process-description"
    ]


def test_get_process_list():
    response = client.get("/processes")
    assert response.status_code == 200
    data = response.json()
    process_list = ProcessList(**data)
    assert len(process_list.processes) > 0  # Adjust based on your mock data


def test_get_process_description():
    assert True


def test_get_job_list():
    assert True


def test_post_execute():
    assert True


def test_get_status():
    job_id = "job1"
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    status_info = StatusInfo(**data)
    assert status_info.jobID == job_id


def test_get_dismiss():
    assert True


def test_get_result():
    assert True
