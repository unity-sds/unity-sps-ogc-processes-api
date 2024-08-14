# coding: utf-8

import importlib
import pkgutil
from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

import openapi_server.impl
from unity_sps_ogc_processes_api.apis.jobs_api_base import BaseJobsApi
from unity_sps_ogc_processes_api.models.exception import Exception
from unity_sps_ogc_processes_api.models.extra_models import TokenModel  # noqa: F401
from unity_sps_ogc_processes_api.models.inline_or_ref_data import InlineOrRefData
from unity_sps_ogc_processes_api.models.job_list import JobList
from unity_sps_ogc_processes_api.models.status_info import StatusInfo

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/jobs/{jobId}",
    responses={
        200: {"model": StatusInfo, "description": "The status of a job."},
        404: {
            "model": Exception,
            "description": "The requested resource does not exist on the server. For example, a path parameter had an incorrect value.",
        },
        500: {"model": Exception, "description": "A server error occurred."},
    },
    tags=["Jobs"],
    summary="cancel a job execution, remove a finished job",
    response_model_by_alias=True,
)
async def dismiss(
    jobId: str = Path(..., description="local identifier of a job"),
) -> StatusInfo:
    """Cancel a job execution and remove it from the jobs list.  For more information, see [Section 14]https://docs.ogc.org/is/18-062r2/18-062r2.html#Dismiss)."""
    return BaseJobsApi.subclasses[0]().dismiss(jobId)


@router.get(
    "/jobs",
    responses={
        200: {"model": JobList, "description": "A list of jobs for this process."},
        404: {
            "model": Exception,
            "description": "The requested resource does not exist on the server. For example, a path parameter had an incorrect value.",
        },
    },
    tags=["Jobs"],
    summary="retrieve the list of jobs.",
    response_model_by_alias=True,
)
async def get_jobs() -> JobList:
    """Lists available jobs.  For more information, see [Section 12](https://docs.ogc.org/is/18-062r2/18-062r2.html#Job_list)."""
    return BaseJobsApi.subclasses[0]().get_jobs()


@router.get(
    "/jobs/{jobId}/results",
    responses={
        200: {
            "model": Dict[str, InlineOrRefData],
            "description": "The processing results of a job.",
        },
        404: {
            "model": Exception,
            "description": "The requested resource does not exist on the server. For example, a path parameter had an incorrect value.",
        },
        500: {"model": Exception, "description": "A server error occurred."},
    },
    tags=["Jobs"],
    summary="retrieve the result(s) of a job",
    response_model_by_alias=True,
)
async def get_result(
    jobId: str = Path(..., description="local identifier of a job"),
    prefer: str = Header(
        None,
        description="Indicates client preferences, such as whether the client wishes a self-contained or minimal response. A &#x60;return&#x3D;minimal&#x60; preference indicates that the client would prefer that links be returned to larger object to minimize the response payload. A &#x60;return&#x3D;representation&#x60; indicates that the client would prefer if the server can return a self-contained response.",
    ),
) -> Dict[str, InlineOrRefData]:
    """Lists available results of a job. In case of a failure, lists exceptions instead.  For more information, see [Section 7.11](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_retrieve_job_results)."""
    return BaseJobsApi.subclasses[0]().get_result(jobId, prefer)


@router.get(
    "/jobs/{jobId}",
    responses={
        200: {"model": StatusInfo, "description": "The status of a job."},
        404: {
            "model": Exception,
            "description": "The requested resource does not exist on the server. For example, a path parameter had an incorrect value.",
        },
        500: {"model": Exception, "description": "A server error occurred."},
    },
    tags=["Jobs"],
    summary="retrieve the status of a job",
    response_model_by_alias=True,
)
async def get_status(
    jobId: str = Path(..., description="local identifier of a job"),
) -> StatusInfo:
    """Shows the status of a job.   For more information, see [Section 7.10](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_retrieve_status_info)."""
    return BaseJobsApi.subclasses[0]().get_status(jobId)
