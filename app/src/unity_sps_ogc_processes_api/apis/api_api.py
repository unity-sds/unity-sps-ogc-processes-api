# coding: utf-8

import importlib
import pkgutil

from fastapi import APIRouter, Query

import openapi_server.impl
from unity_sps_ogc_processes_api.apis.api_api_base import BaseAPIApi
from unity_sps_ogc_processes_api.models.enumeration import Enumeration
from unity_sps_ogc_processes_api.models.exception import Exception

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/api",
    responses={
        200: {"model": object, "description": "The OpenAPI definition of the API."},
        406: {
            "model": Exception,
            "description": "Content negotiation failed. For example, the &#x60;Accept&#x60; header submitted in the request did not support any of the media types supported by the server for the requested resource.",
        },
        500: {"model": Exception, "description": "A server error occurred."},
    },
    tags=["API"],
    summary="Retrieve this API definition.",
    response_model_by_alias=True,
)
async def get_api(
    f: str = Query(
        None,
        description="The format of the response. If no value is provided, the accept header is used to determine the format. Accepted values are &#39;json&#39; or &#39;html&#39;.",
        alias="f",
    ),
) -> object:
    return BaseAPIApi.subclasses[0]().get_api(f)


@router.get(
    "/api/processes-list",
    responses={
        200: {
            "model": Enumeration,
            "description": "An enumerated list of valid string values for API parameters.",
        },
        404: {
            "model": Exception,
            "description": "The requested resource does not exist on the server. For example, a path parameter had an incorrect value.",
        },
        406: {
            "model": Exception,
            "description": "Content negotiation failed. For example, the &#x60;Accept&#x60; header submitted in the request did not support any of the media types supported by the server for the requested resource.",
        },
        500: {"model": Exception, "description": "A server error occurred."},
    },
    tags=["API"],
    summary="Retrieve the list of processes available from this API implementation &amp; deployment.",
    response_model_by_alias=True,
)
async def get_api_processes(
    f: str = Query(
        None,
        description="The format of the response. If no value is provided, the accept header is used to determine the format. Accepted values are &#39;json&#39; or &#39;html&#39;.",
        alias="f",
    ),
) -> Enumeration:
    return BaseAPIApi.subclasses[0]().get_api_processes(f)
