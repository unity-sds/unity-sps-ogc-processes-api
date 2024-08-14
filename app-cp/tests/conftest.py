import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from unity_sps_ogc_processes_api.main import app as application


@pytest.fixture
def app() -> FastAPI:
    application.dependency_overrides = {}

    return application


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)
