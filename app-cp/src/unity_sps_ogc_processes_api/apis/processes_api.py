# coding: utf-8

import importlib
import pkgutil

from fastapi import APIRouter, Body, Header, Path, Query

import openapi_server.impl
from unity_sps_ogc_processes_api.apis.processes_api_base import BaseProcessesApi
from unity_sps_ogc_processes_api.models.exception import Exception
from unity_sps_ogc_processes_api.models.execute200_response import Execute200Response
from unity_sps_ogc_processes_api.models.execute_workflows import ExecuteWorkflows
from unity_sps_ogc_processes_api.models.process import Process
from unity_sps_ogc_processes_api.models.process_list import ProcessList
from unity_sps_ogc_processes_api.models.status_info import StatusInfo

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/processes/{processId}/execution",
    responses={
        200: {
            "model": Execute200Response,
            "description": "Result of synchronous execution",
        },
        201: {
            "model": StatusInfo,
            "description": "Started asynchronous execution. Created job.",
        },
        303: {
            "description": "For _Collection Output_ execution, redirection to an OGC API landing page or collection."
        },
        404: {
            "model": Exception,
            "description": "The requested resource does not exist on the server. For example, a path parameter had an incorrect value.",
        },
        500: {"model": Exception, "description": "A server error occurred."},
    },
    tags=["Processes"],
    summary="execute a process.",
    response_model_by_alias=True,
)
async def execute(
    processId: str = Path(..., description=""),
    execute_workflows: ExecuteWorkflows = Body(
        None,
        description="An execution request specifying any inputs for the process to execute, and optionally to select specific outputs.",
    ),
    response: str = Query(
        None,
        description="For executing the process using the _Collection Output_ mechanism, where the client is redirected (_303_ status) to either an OGC API landing page or collection resource, from which one or more OGC API data access mechanism is available. Data access requests may trigger processing on-demand for a given area, time and resolution of interest.",
        alias="response",
    ),
    prefer: str = Header(
        None,
        description="Indicates client preferences, including whether the client is capable of asynchronous processing. A &#x60;respond-async&#x60; preference indicates a preference for asynchronous processing. A &#x60;wait: &lt;x&gt;s&#x60; preference indicates that the client prefers to wait up to x seconds to receive a reponse synchronously before the server falls back to asynchronous processing.",
    ),
) -> Execute200Response:
    """Executes a process (this may result in the creation of a job resource e.g., for _asynchronous execution_).  For more information, see [Section 7.9](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_create_job)."""
    return BaseProcessesApi.subclasses[0]().execute(
        processId, execute_workflows, response, prefer
    )


@router.get(
    "/processes/{processId}",
    responses={
        200: {"model": Process, "description": "A process description."},
        404: {
            "model": Exception,
            "description": "The requested resource does not exist on the server. For example, a path parameter had an incorrect value.",
        },
    },
    tags=["Processes"],
    summary="retrieve a process description",
    response_model_by_alias=True,
)
async def get_process_description(
    processId: str = Path(..., description=""),
) -> Process:
    """The process description contains information about inputs and outputs and a link to the execution-endpoint for the process. The Core does not mandate the use of a specific process description to specify the interface of a process. That said, the Core requirements class makes the following recommendation:  Implementations SHOULD consider supporting the OGC process description.  For more information, see [Section 7.8](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_process_description)."""
    return BaseProcessesApi.subclasses[0]().get_process_description(processId)


@router.get(
    "/processes",
    responses={
        200: {
            "model": ProcessList,
            "description": "Information about the available processes",
        },
    },
    tags=["Processes"],
    summary="retrieve the list of available processes",
    response_model_by_alias=True,
)
async def get_processes() -> ProcessList:
    """The list of processes contains a summary of each process the OGC API - Processes offers, including the link to a more detailed description of the process.  For more information, see [Section 7.7]https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_process_list)."""
    return BaseProcessesApi.subclasses[0]().get_processes()
