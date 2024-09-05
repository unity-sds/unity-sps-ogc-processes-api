# coding: utf-8

import importlib
import pkgutil

import openapi_server.impl
from fastapi import APIRouter, Query
from unity_sps_ogc_processes_api.apis.conformance_api_base import BaseConformanceApi
from unity_sps_ogc_processes_api.models.conf_classes import ConfClasses
from unity_sps_ogc_processes_api.models.exception import Exception

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/conformance",
    responses={
        200: {
            "model": ConfClasses,
            "description": "The URIs of all conformance classes supported by the server  To support \\&quot;generic\\&quot; clients that want to access multiple OGC API - Processes implementations - and not \\&quot;just\\&quot; a specific API / server, the server declares the conformance classes it implements and conforms to.",
        },
        406: {
            "model": Exception,
            "description": "Content negotiation failed. For example, the &#x60;Accept&#x60; header submitted in the request did not support any of the media types supported by the server for the requested resource.",
        },
        500: {"model": Exception, "description": "A server error occurred."},
    },
    tags=["Conformance"],
    summary="Retrieve the set of OGC API conformance classes that are supported by this service.",
    response_model_by_alias=True,
)
async def get_conformance(
    f: str = Query(
        None,
        description="The format of the response. If no value is provided, the accept header is used to determine the format. Accepted values are &#39;json&#39; or &#39;html&#39;.",
        alias="f",
    ),
) -> ConfClasses:
    return BaseConformanceApi.subclasses[0]().get_conformance()
