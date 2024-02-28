from fastapi.testclient import TestClient
from .main import app
from .models.ogc_processes import LandingPage, ProcessList, StatusInfo

client = TestClient(app)


def test_get_landing_page():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    landing_page = LandingPage(**data)
    assert landing_page.title == "Unity SPS Processing Server"


def test_get_processes():
    response = client.get("/processes")
    assert response.status_code == 200
    data = response.json()
    process_list = ProcessList(**data)
    assert len(process_list.processes) > 0  # Adjust based on your mock data


def test_get_job_status():
    job_id = "job1"
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    status_info = StatusInfo(**data)
    assert status_info.jobID == job_id
