import json
import os
import re

import fakeredis
import pytest
from fastapi import status

# from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from openapi_server.database import Base
from openapi_server.database.models import Process
from openapi_server.utils.redis import RedisLock
from unity_sps_ogc_processes_api.dependencies import (
    get_db,
    get_redis_locking_client,
    get_settings,
)
from unity_sps_ogc_processes_api.main import app

settings = get_settings()
SQLALCHEMY_DATABASE_URL = settings.DB_URL
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


def override_get_redis_locking_client():
    redis_client = fakeredis.FakeRedis(decode_responses=True, version=(6,))
    return RedisLock(redis_client)


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_redis_locking_client] = override_get_redis_locking_client


@pytest.fixture(scope="session")
def test_directory():
    """Returns the directory path of the current test session."""
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session", autouse=True)
def fake_filesystem(fs_session, test_directory):  # pylint:disable=invalid-name
    """Variable name 'fs' causes a pylint warning. Provide a longer name
    acceptable to pylint for use in tests.
    """
    fs_session.add_real_directory(
        os.path.join(test_directory, "..", "..", "process_descriptions")
    )
    fs_session.add_real_directory(os.path.join(test_directory), "test_data")
    fs_session.create_dir(settings.DAG_CATALOG_DIRECTORY)
    fs_session.create_file(
        os.path.join(settings.DAG_CATALOG_DIRECTORY, "cwltool_help_dag.py"),
        contents="test",
    )
    fs_session.create_file(
        os.path.join(settings.DAG_CATALOG_DIRECTORY, "EchoProcess.py"), contents="test"
    )
    fs_session.create_dir(settings.DEPLOYED_DAGS_DIRECTORY)
    yield fs_session


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def mock_get_existing_dag(requests_mock):
    return requests_mock.get(
        re.compile(f"{settings.EMS_API_URL}/dags/([^/]*)$"),
        [
            {
                "json": {
                    "dag_id": "string",
                    "dag_display_name": "string",
                    "root_dag_id": "string",
                    "is_paused": False,
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
                    "schedule_interval": {
                        "__type": "string",
                        "days": 0,
                        "seconds": 0,
                        "microseconds": 0,
                    },
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
                }
            },
            {
                "json": {
                    "dag_id": "string",
                    "dag_display_name": "string",
                    "root_dag_id": "string",
                    "is_paused": True,
                    "is_active": False,
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
                    "schedule_interval": {
                        "__type": "string",
                        "days": 0,
                        "seconds": 0,
                        "microseconds": 0,
                    },
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
                }
            },
        ],
    )


@pytest.fixture(scope="function", autouse=True)
def mock_patch_existing_dag(requests_mock):
    return requests_mock.patch(
        re.compile(f"{settings.EMS_API_URL}/dags/([^/]*)$"),
        [
            {
                "json": {
                    "dag_id": "string",
                    "dag_display_name": "string",
                    "root_dag_id": "string",
                    "is_paused": False,
                    "is_active": True,
                    "is_subdag": True,
                    "last_parsed_time": "2019-08-24T14:15:22Z",
                    "last_pickled": "2019-08-24T14:15:22Z",
                    "last_expired": "2019-08-24T14:15:22Z",
                    "scheduler_lock": True,
                    "pickle_id": "string",
                    "default_view": "string",
                    "fileloc": "string",
                    "file_token": "string",
                    "owners": ["string"],
                    "description": "string",
                    "schedule_interval": {
                        "__type": "string",
                        "days": 0,
                        "seconds": 0,
                        "microseconds": 0,
                    },
                    "timetable_description": "string",
                    "tags": [{"name": "string"}],
                    "max_active_tasks": 0,
                    "max_active_runs": 0,
                    "has_task_concurrency_limits": True,
                    "has_import_errors": True,
                    "next_dagrun": "2019-08-24T14:15:22Z",
                    "next_dagrun_data_interval_start": "2019-08-24T14:15:22Z",
                    "next_dagrun_data_interval_end": "2019-08-24T14:15:22Z",
                    "next_dagrun_create_after": "2019-08-24T14:15:22Z",
                }
            },
            {
                "json": {
                    "dag_id": "string",
                    "dag_display_name": "string",
                    "root_dag_id": "string",
                    "is_paused": True,
                    "is_active": False,
                    "is_subdag": True,
                    "last_parsed_time": "2019-08-24T14:15:22Z",
                    "last_pickled": "2019-08-24T14:15:22Z",
                    "last_expired": "2019-08-24T14:15:22Z",
                    "scheduler_lock": True,
                    "pickle_id": "string",
                    "default_view": "string",
                    "fileloc": "string",
                    "file_token": "string",
                    "owners": ["string"],
                    "description": "string",
                    "schedule_interval": {
                        "__type": "string",
                        "days": 0,
                        "seconds": 0,
                        "microseconds": 0,
                    },
                    "timetable_description": "string",
                    "tags": [{"name": "string"}],
                    "max_active_tasks": 0,
                    "max_active_runs": 0,
                    "has_task_concurrency_limits": True,
                    "has_import_errors": True,
                    "next_dagrun": "2019-08-24T14:15:22Z",
                    "next_dagrun_data_interval_start": "2019-08-24T14:15:22Z",
                    "next_dagrun_data_interval_end": "2019-08-24T14:15:22Z",
                    "next_dagrun_create_after": "2019-08-24T14:15:22Z",
                }
            },
        ],
    )


@pytest.fixture(scope="function", autouse=True)
def mock_delete_existing_dag(requests_mock):
    return requests_mock.delete(
        re.compile(f"{settings.EMS_API_URL}/dags/([^/]*)$"),
        status_code=status.HTTP_204_NO_CONTENT,
    )


@pytest.fixture(scope="function", autouse=True)
def mock_post_existing_dag_new_dagrun(requests_mock):
    return requests_mock.post(
        re.compile(f"{settings.EMS_API_URL}/dags/([^/]*)/dagRuns$"),
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
def mock_get_existing_dag_dagruns(requests_mock):
    return requests_mock.get(
        re.compile(f"{settings.EMS_API_URL}/dags/([^/]*)/dagRuns$"),
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
def mock_get_existing_running_dag_dagruns(requests_mock):
    return requests_mock.get(
        re.compile(f"{settings.EMS_API_URL}/dags/([^/]*)/dagRuns\\?state=running$"),
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
                    "state": "running",
                    "external_trigger": True,
                    "conf": {},
                    "note": "string",
                }
            ],
            "total_entries": 1,
        },
    )


@pytest.fixture(scope="function", autouse=True)
def mock_patch_existing_running_dag_dagrun(requests_mock):
    return requests_mock.patch(
        re.compile(f"{settings.EMS_API_URL}/dags/([^/]*)/dagRuns/([^/]*)$"),
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
def mock_get_existing_dag_dagrun(requests_mock):
    return requests_mock.get(
        re.compile(f"{settings.EMS_API_URL}/dags/([^/]*)/dagRuns/([^/]*)$"),
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
def mock_delete_existing_dag_dagrun(requests_mock):
    return requests_mock.delete(
        re.compile(f"{settings.EMS_API_URL}/dags/([^/]*)/dagRuns/([^/]*)$"),
        status_code=status.HTTP_204_NO_CONTENT,
    )


@pytest.fixture(scope="function", autouse=True)
def mock_get_existing_running_dag_dagrun_tasks(requests_mock):
    return requests_mock.get(
        re.compile(
            f"{settings.EMS_API_URL}/dags/([^/]*)/dagRuns/([^/]*)/taskInstances$"
        ),
        json={
            "task_instances": [
                {
                    "task_id": "string",
                    "task_display_name": "string",
                    "dag_id": "string",
                    "dag_run_id": "string",
                    "execution_date": "string",
                    "start_date": "string",
                    "end_date": "string",
                    "duration": 0,
                    "state": None,
                    "try_number": 0,
                    "map_index": 0,
                    "max_tries": 0,
                    "hostname": "string",
                    "unixname": "string",
                    "pool": "string",
                    "pool_slots": 0,
                    "queue": "string",
                    "priority_weight": 0,
                    "operator": "string",
                    "queued_when": "string",
                    "pid": 0,
                    "executor_config": "string",
                    "sla_miss": {
                        "task_id": "string",
                        "dag_id": "string",
                        "execution_date": "string",
                        "email_sent": True,
                        "timestamp": "string",
                        "description": "string",
                        "notification_sent": True,
                    },
                    "rendered_map_index": "string",
                    "rendered_fields": {},
                    "trigger": {
                        "id": 0,
                        "classpath": "string",
                        "kwargs": "string",
                        "created_date": "string",
                        "triggerer_id": 0,
                    },
                    "triggerer_job": {
                        "id": 0,
                        "dag_id": "string",
                        "state": "string",
                        "job_type": "string",
                        "start_date": "string",
                        "end_date": "string",
                        "latest_heartbeat": "string",
                        "executor_class": "string",
                        "hostname": "string",
                        "unixname": "string",
                    },
                    "note": "string",
                }
            ],
            "total_entries": 0,
        },
    )


@pytest.fixture(scope="function", autouse=True)
def mock_patch_existing_running_dag_dagrun_task(requests_mock):
    return requests_mock.patch(
        re.compile(
            f"{settings.EMS_API_URL}/dags/([^/]*)/dagRuns/([^/]*)/taskInstances/([^/]*)$"
        ),
        json={
            "task_id": "string",
            "dag_id": "string",
            "execution_date": "string",
            "dag_run_id": "string",
        },
    )


@pytest.fixture(scope="function")
def deploy_process(test_directory, client):
    data_filename = os.path.join(
        test_directory, "..", "process_descriptions", "cwltool_help_dag.json"
    )
    f = open(data_filename)
    process_json = json.load(f)
    process = Process.model_validate(process_json)
    response = client.post("/processes", json=process.model_dump())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    process = Process.model_validate(data)
    assert process.id == "cwltool_help_dag"

    yield process

    response = client.delete(f"/processes/{process.id}", params={"force": True})
    assert response.status_code == status.HTTP_204_NO_CONTENT


# @pytest.fixture(scope="function")
# def execute_process(
#     test_directory, mock_post_existing_dag_new_dagrun, client, deploy_process
# ):
#     data_filename = os.path.join(
#         test_directory, "test_data/execution_requests/execute_cwltool_help_dag.json"
#     )
#     f = open(data_filename)
#     execute_json = json.load(f)
#     execute = Execute.model_validate(execute_json)
#     response = client.post(
#         f"/processes/{deploy_process.id}/execution", json=jsonable_encoder(execute)
#     )
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     status_info = StatusInfo.model_validate(data)

#     yield status_info

#     response = client.delete(f"/jobs/{status_info.jobID}")
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     status_info = StatusInfo.model_validate(data)
#     assert status_info.status == StatusCode.dismissed.value
