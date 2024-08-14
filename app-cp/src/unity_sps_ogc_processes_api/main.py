# coding: utf-8

"""
    OGC API - Processes

    Example API Definition for OGC API - Processes

    The version of the OpenAPI document: 0.1
    Contact: info@ogc.org
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from fastapi import FastAPI

from unity_sps_ogc_processes_api.apis.api_api import router as APIApiRouter
from unity_sps_ogc_processes_api.apis.conformance_api import (
    router as ConformanceApiRouter,
)
from unity_sps_ogc_processes_api.apis.dru_api import router as DRUApiRouter
from unity_sps_ogc_processes_api.apis.jobs_api import router as JobsApiRouter
from unity_sps_ogc_processes_api.apis.landing_page_api import (
    router as LandingPageApiRouter,
)
from unity_sps_ogc_processes_api.apis.processes_api import router as ProcessesApiRouter

app = FastAPI(
    title="OGC API - Processes",
    description="Example API Definition for OGC API - Processes",
    version="0.1",
)

app.include_router(APIApiRouter)
app.include_router(ConformanceApiRouter)
app.include_router(DRUApiRouter)
app.include_router(JobsApiRouter)
app.include_router(LandingPageApiRouter)
app.include_router(ProcessesApiRouter)
