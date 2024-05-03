import json
import os

import pytest
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


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def test_directory():
    """Returns the directory path of the current test session."""
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session")
def deploy_process(test_directory, client):
    data_filename = os.path.join(test_directory, "..", "process_definitions", "cwltool_help_dag.json")
    f = open(data_filename)
    process_json = json.load(f)
    process = Process.model_validate(process_json)
    response = client.post("/processes", json=process.model_dump())
    assert response.status_code == 200
    data = response.json()
    process = Process.model_validate(data)
    assert process.id == "cwltool_help_dag"

    yield process

    response = client.delete(f"/processes/{process.id}")
    assert response.status_code == 204


@pytest.fixture(scope="session")
def execute_process(test_directory, client, deploy_process):
    data_filename = os.path.join(test_directory, "test_data/execution_requests/execute_cwltool_help_dag.json")
    f = open(data_filename)
    execute_json = json.load(f)
    execute = Execute.model_validate(execute_json)
    response = client.post(f"/processes/{deploy_process.id}/execution", json=jsonable_encoder(execute))
    assert response.status_code == 200
    data = response.json()
    status_info = StatusInfo.model_validate(data)

    yield status_info

    response = client.delete(f"/jobs/{status_info.jobID}")
    assert response.status_code == 200
    data = response.json()
    status_info = StatusInfo.model_validate(data)
    assert status_info.status == StatusCode.dismissed.value
