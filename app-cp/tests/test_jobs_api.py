# coding: utf-8

from fastapi.testclient import TestClient

from unity_sps_ogc_processes_api.models.exception import Exception  # noqa: F401
from unity_sps_ogc_processes_api.models.inline_or_ref_data import (  # noqa: F401
    InlineOrRefData,
)
from unity_sps_ogc_processes_api.models.job_list import JobList  # noqa: F401
from unity_sps_ogc_processes_api.models.status_info import StatusInfo  # noqa: F401


def test_dismiss(client: TestClient):
    """Test case for dismiss

    cancel a job execution, remove a finished job
    """

    # uncomment below to make a request
    # response = client.request(
    #    "DELETE",
    #    "/jobs/{jobId}".format(jobId='job_id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_jobs(client: TestClient):
    """Test case for get_jobs

    retrieve the list of jobs.
    """

    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/jobs",
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_result(client: TestClient):
    """Test case for get_result

    retrieve the result(s) of a job
    """

    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/jobs/{jobId}/results".format(jobId='job_id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_status(client: TestClient):
    """Test case for get_status

    retrieve the status of a job
    """

    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/jobs/{jobId}".format(jobId='job_id_example'),
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
