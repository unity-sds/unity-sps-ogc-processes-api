# coding: utf-8

from fastapi.testclient import TestClient

from unity_sps_ogc_processes_api.models.enumeration import Enumeration  # noqa: F401
from unity_sps_ogc_processes_api.models.exception import Exception  # noqa: F401


def test_get_api(client: TestClient):
    """Test case for get_api

    Retrieve this API definition.
    """
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/api",
    #    headers=headers,
    #    params=params,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_api_processes(client: TestClient):
    """Test case for get_api_processes

    Retrieve the list of processes available from this API implementation & deployment.
    """
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/api/processes-list",
    #    headers=headers,
    #    params=params,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
