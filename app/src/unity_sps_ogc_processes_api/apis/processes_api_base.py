# coding: utf-8

from typing import ClassVar, Tuple

from unity_sps_ogc_processes_api.models.execute200_response import Execute200Response
from unity_sps_ogc_processes_api.models.execute_workflows import ExecuteWorkflows
from unity_sps_ogc_processes_api.models.process import Process
from unity_sps_ogc_processes_api.models.process_list import ProcessList


class BaseProcessesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseProcessesApi.subclasses = BaseProcessesApi.subclasses + (cls,)

    def execute(
        self,
        processId: str,
        execute_workflows: ExecuteWorkflows,
        response: str,
        prefer: str,
    ) -> Execute200Response:
        """Executes a process (this may result in the creation of a job resource e.g., for _asynchronous execution_).  For more information, see [Section 7.9](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_create_job)."""
        ...

    def get_process_description(
        self,
        processId: str,
    ) -> Process:
        """The process description contains information about inputs and outputs and a link to the execution-endpoint for the process. The Core does not mandate the use of a specific process description to specify the interface of a process. That said, the Core requirements class makes the following recommendation:  Implementations SHOULD consider supporting the OGC process description.  For more information, see [Section 7.8](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_process_description)."""
        ...

    def get_processes(
        self,
    ) -> ProcessList:
        """The list of processes contains a summary of each process the OGC API - Processes offers, including the link to a more detailed description of the process.  For more information, see [Section 7.7]https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_process_list)."""
        ...
