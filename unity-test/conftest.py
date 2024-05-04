import json
import os

import pytest
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app, get_db, get_settings
from app.schemas.ogc_processes import Execute, Process, StatusCode, StatusInfo

settings = get_settings()
SQLALCHEMY_DATABASE_URL = settings.db_url
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# @pytest.fixture(scope="session")
# def fake_filesystem(fs):  # pylint:disable=invalid-name
#     """Variable name 'fs' causes a pylint warning. Provide a longer name
#     acceptable to pylint for use in tests.
#     """
#     yield fs


# @pytest.fixture(scope="session", autouse=True)
# def static_dags_directory(fake_filesystem):
#     file_path = "/static-dags"
#     fake_filesystem.create_dir(file_path)
#     assert os.path.isdir(file_path)


# @pytest.fixture(scope="session", autouse=True)
# def deployed_dags_directory(fake_filesystem):
#     file_path = "/deployed-dags"
#     fake_filesystem.create_dir(file_path)
#     assert os.path.isdir(file_path)


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def test_directory():
    """Returns the directory path of the current test session."""
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="function", autouse=True)
def mock_get_existing_dag(requests_mock, deploy_process):
    return requests_mock.get(
        f"{settings.ems_api_url}/dags/{deploy_process.id}",
        json={
            "dag_id": deploy_process.id,
            "dag_display_name": "string",
            "root_dag_id": "string",
            "is_paused": True,
            "is_active": True,
            "is_subdag": True,
            "last_parsed_time": "2019-08-24T14:15:22.548326+00:00",
            "last_pickled": "2019-08-24T14:15:22.548326+00:00",
            "last_expired": "2019-08-24T14:15:22.548326+00:00",
            "scheduler_lock": True,
            "pickle_id": "string",
            "default_view": "string",
            "fileloc": "string",
            "file_token": "string",
            "owners": ["string"],
            "description": "string",
            "schedule_interval": {"__type": "string", "days": 0, "seconds": 0, "microseconds": 0},
            "timetable_description": "string",
            "tags": [{"name": "string"}],
            "max_active_tasks": 0,
            "max_active_runs": 0,
            "has_task_concurrency_limits": True,
            "has_import_errors": True,
            "next_dagrun": "2019-08-24T14:15:22.548326+00:00",
            "next_dagrun_data_interval_start": "2019-08-24T14:15:22.548326+00:00",
            "next_dagrun_data_interval_end": "2019-08-24T14:15:22.548326+00:00",
            "next_dagrun_create_after": "2019-08-24T14:15:22.548326+00:00",
        },
    )


@pytest.fixture(scope="function", autouse=True)
def mock_delete_existing_dag(requests_mock, deploy_process):
    return requests_mock.get(
        f"{settings.ems_api_url}/dags/{deploy_process.id}", status_code=status.HTTP_204_NO_CONTENT
    )


@pytest.fixture(scope="function", autouse=True)
def mock_post_existing_dag_new_dagrun(requests_mock, deploy_process):
    return requests_mock.post(
        f"{settings.ems_api_url}/dags/{deploy_process.id}/dagRuns",
        json={
            "dag_run_id": "string",
            "logical_date": "2019-08-24T14:15:22Z",
            "execution_date": "2019-08-24T14:15:22Z",
            "data_interval_start": "2019-08-24T14:15:22Z",
            "data_interval_end": "2019-08-24T14:15:22Z",
            "conf": {},
            "note": "string",
        },
    )


@pytest.fixture(scope="function", autouse=True)
def mock_get_existing_dag_dagruns(requests_mock, deploy_process):
    return requests_mock.get(
        f"{settings.ems_api_url}/dags/{deploy_process.id}/dagRuns",
        json={
            "dag_runs": [
                {
                    "dag_run_id": "string",
                    "dag_id": "string",
                    "logical_date": "2019-08-24T14:15:22.548326+00:00",
                    "execution_date": "2019-08-24T14:15:22.548326+00:00",
                    "start_date": "2019-08-24T14:15:22.548326+00:00",
                    "end_date": "2019-08-24T14:15:22.548326+00:00",
                    "data_interval_start": "2019-08-24T14:15:22.548326+00:00",
                    "data_interval_end": "2019-08-24T14:15:22.548326+00:00",
                    "last_scheduling_decision": "2019-08-24T14:15:22.548326+00:00",
                    "run_type": "backfill",
                    "state": "queued",
                    "external_trigger": True,
                    "conf": {},
                    "note": "string",
                }
            ],
            "total_entries": 1,
        },
    )


@pytest.fixture(scope="function", autouse=True)
def mock_get_existing_dag_dagrun(requests_mock, execute_process):
    return requests_mock.get(
        f"{settings.ems_api_url}/dags/{execute_process.processID}/dagRuns/{execute_process.jobID}",
        json={
            "dag_run_id": "string",
            "dag_id": "string",
            "logical_date": "2019-08-24T14:15:22.548326+00:00",
            "execution_date": "2019-08-24T14:15:22.548326+00:00",
            "start_date": "2019-08-24T14:15:22.548326+00:00",
            "end_date": "2019-08-24T14:15:22.548326+00:00",
            "data_interval_start": "2019-08-24T14:15:22.548326+00:00",
            "data_interval_end": "2019-08-24T14:15:22.548326+00:00",
            "last_scheduling_decision": "2019-08-24T14:15:22.548326+00:00",
            "run_type": "backfill",
            "state": "queued",
            "external_trigger": True,
            "conf": {},
            "note": "string",
        },
    )


@pytest.fixture(scope="function", autouse=True)
def mock_delete_existing_dag_dagrun(requests_mock, execute_process):
    return requests_mock.delete(
        f"{settings.ems_api_url}/dags/{execute_process.processID}/dagRuns/{execute_process.jobID}",
        status_code=status.HTTP_204_NO_CONTENT,
    )


@pytest.fixture(scope="function")
def deploy_process(test_directory, client):
    data_filename = os.path.join(test_directory, "..", "process_descriptions", "cwltool_help_dag.json")
    f = open(data_filename)
    process_json = json.load(f)
    process = Process.model_validate(process_json)
    response = client.post("/processes", json=process.model_dump())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    process = Process.model_validate(data)
    assert process.id == "cwltool_help_dag"

    yield process

    response = client.delete(f"/processes/{process.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.fixture(scope="function")
def execute_process(test_directory, mock_post_existing_dag_new_dagrun, client, deploy_process):
    data_filename = os.path.join(test_directory, "test_data/execution_requests/execute_cwltool_help_dag.json")
    f = open(data_filename)
    execute_json = json.load(f)
    execute = Execute.model_validate(execute_json)
    response = client.post(f"/processes/{deploy_process.id}/execution", json=jsonable_encoder(execute))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    status_info = StatusInfo.model_validate(data)

    yield status_info

    response = client.delete(f"/jobs/{status_info.jobID}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    status_info = StatusInfo.model_validate(data)
    assert status_info.status == StatusCode.dismissed.value
