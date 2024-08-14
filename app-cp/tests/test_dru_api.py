# coding: utf-8

from fastapi.testclient import TestClient

from unity_sps_ogc_processes_api.models.exception import Exception  # noqa: F401
from unity_sps_ogc_processes_api.models.ogcapppkg import Ogcapppkg  # noqa: F401
from unity_sps_ogc_processes_api.models.processes_list import (  # noqa: F401
    ProcessesList,
)


def test_deploy(client: TestClient):
    """Test case for deploy

    deploy a process.
    """
    Ogcapppkg()
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/processes",
    #    headers=headers,
    #    json=ogcapppkg,
    #    params=params,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_replace(client: TestClient):
    """Test case for replace

    replace a process.
    """
    Ogcapppkg()

    # uncomment below to make a request
    # response = client.request(
    #    "PUT",
    #    "/processes/{processId}".format(processId=unity_sps_ogc_processes_api.ProcessesList()),
    #    headers=headers,
    #    json=ogcapppkg,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_undeploy(client: TestClient):
    """Test case for undeploy

    undeploy a process.
    """

    # uncomment below to make a request
    # response = client.request(
    #    "DELETE",
    #    "/processes/{processId}".format(processId=unity_sps_ogc_processes_api.ProcessesList()),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
