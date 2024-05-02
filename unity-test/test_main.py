from app.schemas.ogc_processes import (
    ConfClasses,
    JobList,
    LandingPage,
    Process,
    ProcessList,
    Results,
    StatusInfo,
)


def test_get_landing_page(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    landing_page = LandingPage.model_validate(data)
    assert landing_page.title == "Unity SPS Processing Server"


def test_get_conformance_declaration(client):
    response = client.get("/conformance")
    assert response.status_code == 200
    data = response.json()
    conformance_declaration = ConfClasses.model_validate(data)
    assert len(conformance_declaration.conformsTo) > 0
    assert conformance_declaration.conformsTo == [
        "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/ogc-process-description"
    ]


def test_get_process_description(client, deploy_process):
    response = client.get(f"/processes/{deploy_process.id}")
    assert response.status_code == 200
    data = response.json()
    process = Process.model_validate(data)
    assert process.id == deploy_process.id


def test_get_process_list(client):
    response = client.get("/processes")
    assert response.status_code == 200
    data = response.json()
    assert ProcessList.model_validate(data)


def test_get_job_list(client, execute_process):
    response = client.get("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert JobList.model_validate(data)


def test_get_status(client, execute_process):
    response = client.get(f"/jobs/{execute_process.jobID}")
    assert response.status_code == 200
    data = response.json()
    status_info = StatusInfo.model_validate(data)
    assert status_info.jobID == execute_process.jobID


def test_get_results(client, execute_process):
    response = client.get(f"/jobs/{execute_process.jobID}/results")
    assert response.status_code == 200
    data = response.json()
    assert Results.model_validate(data)
