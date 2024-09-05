# coding: utf-8

import importlib
import pkgutil

import openapi_server.impl
from fastapi import APIRouter
from unity_sps_ogc_processes_api.apis.health_api_base import BaseHealthApi
from unity_sps_ogc_processes_api.models.exception import Exception
from unity_sps_ogc_processes_api.models.health_check import HealthCheck

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/health",
    responses={
        200: {"model": HealthCheck, "description": "The health status of the API."},
        500: {"model": Exception, "description": "A server error occurred."},
    },
    tags=["Health"],
    summary="Retrieve the health status of the API.",
    response_model_by_alias=True,
)
async def get_health() -> HealthCheck:
    """Retrieves the health status of the API."""
    health_api = BaseHealthApi.subclasses[0]()
    return health_api.get_health()
