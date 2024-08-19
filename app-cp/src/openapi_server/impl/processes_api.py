from unity_sps_ogc_processes_api.apis.processes_api_base import BaseProcessesApi
from unity_sps_ogc_processes_api.models.execute200_response import Execute200Response
from unity_sps_ogc_processes_api.models.execute_workflows import ExecuteWorkflows
from unity_sps_ogc_processes_api.models.link import Link
from unity_sps_ogc_processes_api.models.process import Process
from unity_sps_ogc_processes_api.models.process_list import ProcessList
from unity_sps_ogc_processes_api.models.process_summary import ProcessSummary
from unity_sps_ogc_processes_api.models.status_info import StatusInfo


class ProcessesApiImpl(BaseProcessesApi):
    def get_process_description(self, processId: str) -> Process:
        return Process(
            id=processId,
            title="Sample Process",
            description="This is a sample process description",
            version="1.0.0",
            jobControlOptions=["sync-execute", "async-execute"],
            outputTransmission=["value"],
            executeEndpoint=f"http://example.com/api/processes/{processId}/execution",
            inputs={},
            outputs={},
            links=[
                Link(
                    href=f"http://example.com/api/processes/{processId}",
                    rel="self",
                    type="application/json",
                    title="This process",
                )
            ],
        )

    def get_processes(self) -> ProcessList:
        return ProcessList(
            processes=[
                ProcessSummary(
                    id="process1",
                    title="Process 1",
                    description="Description 1",
                    version="1.0.0",
                ),
                ProcessSummary(
                    id="process2",
                    title="Process 2",
                    description="Description 2",
                    version="1.0.0",
                ),
            ],
            links=[
                Link(
                    href="http://example.com/api/processes",
                    rel="self",
                    type="application/json",
                    title="this document",
                )
            ],
        )

    def execute(
        self,
        processId: str,
        execute_workflows: ExecuteWorkflows,
        response: str,
        prefer: str,
    ) -> Execute200Response:
        # Placeholder implementation
        # In a real-world scenario, you would execute the process here
        # and return the appropriate response based on the execution mode

        if prefer == "respond-async":
            # Asynchronous execution
            return StatusInfo(
                type="process",
                job_id="sample_job_id",
                status="accepted",
                message="Process execution started asynchronously",
            )
        else:
            # Synchronous execution
            return Execute200Response(
                outputs={"result": "Sample output for synchronous execution"}
            )
