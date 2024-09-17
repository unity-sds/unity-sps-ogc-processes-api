# coding: utf-8

import json
import os

import pytest
from fastapi.testclient import TestClient
from unity_sps_ogc_processes_api.models.ogcapppkg import Ogcapppkg


@pytest.fixture
def sample_ogcapppkg():
    # Get the current directory of the test file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to echoProcess.json
    json_file_path = os.path.join(current_dir, "echoProcess.json")

    # Read the JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    return Ogcapppkg(**data)


def test_deploy(client: TestClient, sample_ogcapppkg):
    """Test case for deploy"""
    response = client.post(
        "/processes",
        json=sample_ogcapppkg.model_dump(exclude_none=True, by_alias=True),
    )
    assert response.status_code == 201


def test_replace(client: TestClient, sample_ogcapppkg):
    """Test case for replace"""
    process_id = "EchoProcess"
    response = client.put(
        f"/processes/{process_id}",
        json=sample_ogcapppkg.model_dump(),
    )
    assert response.status_code == 204


def test_undeploy(client: TestClient):
    """Test case for undeploy"""
    process_id = "EchoProcess"
    response = client.delete(f"/processes/{process_id}", params={"force": True})
    assert response.status_code == 204


def test_deploy_conflict(client: TestClient, sample_ogcapppkg):
    """Test case for deploy when process already exists"""
    # First, deploy the process
    response = client.post(
        "/processes",
        json=sample_ogcapppkg.model_dump(exclude_none=True, by_alias=True),
    )
    # Try to deploy the same process again
    response = client.post(
        "/processes",
        json=sample_ogcapppkg.model_dump(exclude_none=True, by_alias=True),
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_undeploy_not_found(client: TestClient):
    """Test case for undeploy when process doesn't exist"""
    process_id = "non_existent_process"
    response = client.delete(f"/processes/{process_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
