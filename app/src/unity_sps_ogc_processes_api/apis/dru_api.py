# coding: utf-8

import importlib
import pkgutil

import openapi_server.impl
from fastapi import APIRouter, Body, Depends, Path, Query
from openapi_server.config.config import Settings
from openapi_server.utils.redis import RedisLock
from sqlalchemy.orm import Session
from unity_sps_ogc_processes_api.apis.dru_api_base import BaseDRUApi
from unity_sps_ogc_processes_api.dependencies import get_db, get_redis_locking_client, get_settings
from unity_sps_ogc_processes_api.models.exception import Exception
from unity_sps_ogc_processes_api.models.ogcapppkg import Ogcapppkg

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/processes",
    responses={
        201: {"description": ""},
        403: {"model": Exception, "description": "the processes is not mutable"},
        409: {
            "model": Exception,
            "description": "the processes being added is already deployed (i.e. duplicate)",
        },
        500: {"model": Exception, "description": "A server error occurred."},
    },
    tags=["DRU"],
    summary="deploy a process.",
    response_model_by_alias=True,
)
async def deploy(
    settings: Settings = Depends(get_settings),
    redis_locking_client: RedisLock = Depends(get_redis_locking_client),
    db: Session = Depends(get_db),
    ogcapppkg: Ogcapppkg = Body(None, description="An OGC Application Package used to deploy a new process."),
    w: str = Query(
        None,
        description="Point to the workflow identifier for deploying a CWL containing multiple workflow definitions",
        alias="w",
    ),
) -> None:
    """Deploys a process.  For more information, see [Section 6.3](http://docs.ogc.org/DRAFTS/20-044.html#_87a6983e-d060-458c-95ab-27e232e64822)."""
    dru_api = BaseDRUApi.subclasses[0](settings, redis_locking_client, db)
    return dru_api.deploy(ogcapppkg, w)


@router.put(
    "/processes/{processId}",
    responses={
        204: {"description": "successful operation (no response body)"},
        403: {"model": Exception, "description": "the processes is not mutable"},
        404: {
            "model": Exception,
            "description": "The requested resource does not exist on the server. For example, a path parameter had an incorrect value.",
        },
        409: {
            "model": Exception,
            "description": "the processes being added is already deployed (i.e. duplicate)",
        },
        500: {"model": Exception, "description": "A server error occurred."},
    },
    tags=["DRU"],
    summary="replace a process.",
    response_model_by_alias=True,
)
async def replace(
    settings: Settings = Depends(get_settings),
    redis_locking_client: RedisLock = Depends(get_redis_locking_client),
    db: Session = Depends(get_db),
    processId: str = Path(..., description=""),
    ogcapppkg: Ogcapppkg = Body(None, description="An OGC Application Package used to deploy a new process."),
) -> None:
    """Replaces a process.  For more information, see [Section 6.4](http://docs.ogc.org/DRAFTS/20-044.html#_18582f42-ebc6-4284-9333-c089068f62b6)."""
    dru_api = BaseDRUApi.subclasses[0](settings, redis_locking_client, db)
    return dru_api.replace(processId, ogcapppkg)


@router.delete(
    "/processes/{processId}",
    responses={
        204: {"description": "successful operation (no response body)"},
        403: {"model": Exception, "description": "the processes is not mutable"},
        404: {
            "model": Exception,
            "description": "The requested resource does not exist on the server. For example, a path parameter had an incorrect value.",
        },
        409: {
            "model": Exception,
            "description": "The process has active DAG runs and force is not set to true.",
        },
        500: {"model": Exception, "description": "A server error occurred."},
    },
    tags=["DRU"],
    summary="undeploy a process.",
    response_model_by_alias=True,
)
async def undeploy(
    settings: Settings = Depends(get_settings),
    redis_locking_client: RedisLock = Depends(get_redis_locking_client),
    db: Session = Depends(get_db),
    processId: str = Path(..., description=""),
    force: bool = Query(False, description="Force undeployment even if there are active DAG runs"),
) -> None:
    """Undeploys a process. For more information, see [Section 6.5](http://docs.ogc.org/DRAFTS/20-044.html#_16391f9e-538f-4a84-9710-72a6bab82842)."""
    dru_api = BaseDRUApi.subclasses[0](settings, redis_locking_client, db)
    return dru_api.undeploy(processId, force)
