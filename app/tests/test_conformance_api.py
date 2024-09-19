# coding: utf-8

from fastapi.testclient import TestClient

from unity_sps_ogc_processes_api.models.conf_classes import ConfClasses  # noqa: F401
from unity_sps_ogc_processes_api.models.exception import Exception  # noqa: F401


def test_get_conformance(client: TestClient):
    """Test case for get_conformance

    Retrieve the set of OGC API conformance classes that are supported by this service.
    """
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/conformance",
    #    headers=headers,
    #    params=params,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
