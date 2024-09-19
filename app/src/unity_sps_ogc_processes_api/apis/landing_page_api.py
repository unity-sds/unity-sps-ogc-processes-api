# coding: utf-8

import importlib
import pkgutil

from fastapi import APIRouter, Query

import openapi_server.impl
from unity_sps_ogc_processes_api.apis.landing_page_api_base import BaseLandingPageApi
from unity_sps_ogc_processes_api.models.exception import Exception
from unity_sps_ogc_processes_api.models.landing_page import LandingPage

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/",
    responses={
        200: {
            "model": LandingPage,
            "description": "The landing page provides links to the API definition (link relation &#x60;service-desc&#x60;, in this case path &#x60;/api&#x60;), to the Conformance declaration (path &#x60;/conformance&#x60;, link relation &#x60;http://www.opengis.net/def/rel/ogc/1.0/conformance&#x60;), and to other resources.",
        },
        406: {
            "model": Exception,
            "description": "Content negotiation failed. For example, the &#x60;Accept&#x60; header submitted in the request did not support any of the media types supported by the server for the requested resource.",
        },
        500: {"model": Exception, "description": "A server error occurred."},
    },
    tags=["Landing Page"],
    summary="Retrieve the OGC API landing page for this service.",
    response_model_by_alias=True,
)
async def get_landing_page(
    f: str = Query(
        None,
        description="The format of the response. If no value is provided, the accept header is used to determine the format. Accepted values are &#39;json&#39; or &#39;html&#39;.",
        alias="f",
    ),
) -> LandingPage:
    return BaseLandingPageApi.subclasses[0]().get_landing_page(f)
