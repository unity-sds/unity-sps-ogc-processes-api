from datetime import datetime
from typing import Dict

from unity_sps_ogc_processes_api.apis.jobs_api_base import BaseJobsApi
from unity_sps_ogc_processes_api.models.inline_or_ref_data import InlineOrRefData
from unity_sps_ogc_processes_api.models.job_list import JobList
from unity_sps_ogc_processes_api.models.link import Link
from unity_sps_ogc_processes_api.models.status_code import StatusCode
from unity_sps_ogc_processes_api.models.status_info import StatusInfo


class JobsApiImpl(BaseJobsApi):
    def dismiss(self, jobId: str) -> StatusInfo:
        return StatusInfo(
            type="process",
            job_id=jobId,
            status=StatusCode.DISMISSED,
            message="Job dismissed",
            updated=datetime.now(),
        )

    def get_jobs(self) -> JobList:
        return JobList(
            jobs=[
                StatusInfo(
                    type="process",
                    job_id="job1",
                    status=StatusCode.RUNNING,
                    created=datetime.now(),
                    updated=datetime.now(),
                ),
                StatusInfo(
                    type="process",
                    job_id="job2",
                    status=StatusCode.SUCCESSFUL,
                    created=datetime.now(),
                    started=datetime.now(),
                    finished=datetime.now(),
                    updated=datetime.now(),
                ),
            ],
            links=[
                Link(
                    href="http://example.com/api/jobs",
                    rel="self",
                    type="application/json",
                    title="this document",
                )
            ],
        )

    def get_result(self, jobId: str, prefer: str) -> Dict[str, InlineOrRefData]:
        return {
            "output1": InlineOrRefData(href="http://example.com/result1"),
            "output2": InlineOrRefData(href="http://example.com/result2"),
        }

    def get_status(self, jobId: str) -> StatusInfo:
        return StatusInfo(
            type="process",
            job_id=jobId,
            status=StatusCode.SUCCESSFUL,
            created=datetime.now(),
            started=datetime.now(),
            finished=datetime.now(),
            updated=datetime.now(),
            progress=100,
        )
