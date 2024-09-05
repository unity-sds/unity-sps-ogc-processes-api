# coding: utf-8

from fastapi.testclient import TestClient
from unity_sps_ogc_processes_api.models.exception import Exception  # noqa: F401
from unity_sps_ogc_processes_api.models.landing_page import LandingPage  # noqa: F401


def test_get_landing_page(client: TestClient):
    """Test case for get_landing_page

    Retrieve the OGC API landing page for this service.
    """
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/",
    #    headers=headers,
    #    params=params,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
