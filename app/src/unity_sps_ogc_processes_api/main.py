# coding: utf-8

"""
    OGC API - Processes

    Example API Definition for OGC API - Processes

    The version of the OpenAPI document: 0.1
    Contact: info@ogc.org
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from fastapi import Depends, FastAPI
from openapi_server.database import engine, models
from unity_sps_ogc_processes_api.apis.api_api import router as APIApiRouter
from unity_sps_ogc_processes_api.apis.conformance_api import router as ConformanceApiRouter
from unity_sps_ogc_processes_api.apis.dru_api import router as DRUApiRouter
from unity_sps_ogc_processes_api.apis.health_api import router as HealthApiRouter
from unity_sps_ogc_processes_api.apis.jobs_api import router as JobsApiRouter
from unity_sps_ogc_processes_api.apis.landing_page_api import router as LandingPageApiRouter
from unity_sps_ogc_processes_api.apis.processes_api import router as ProcessesApiRouter
from unity_sps_ogc_processes_api.dependencies import get_db, get_redis_locking_client, get_settings

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    version="2.0.0",
    title="Unity Processing API conforming to the Draft of OGC API - Processes - Part 2: Deploy, Replace, Undeploy",
    description="This document is an API definition document provided alongside the OGC API - Processes standard. The OGC API - Processes Standard specifies a processing interface to communicate over a RESTful protocol using JavaScript Object Notation (JSON) encodings. The specification allows for the wrapping of computational tasks into executable processes that can be offered by a server and be invoked by a client application.",
    license={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    servers=[],
)

app.include_router(APIApiRouter)
app.include_router(ConformanceApiRouter)
app.include_router(
    DRUApiRouter,
    dependencies=[
        Depends(get_settings),
        Depends(get_redis_locking_client),
        Depends(get_db),
    ],
)
app.include_router(JobsApiRouter)
app.include_router(LandingPageApiRouter)
app.include_router(ProcessesApiRouter)
app.include_router(HealthApiRouter)