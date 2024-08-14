# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from unity_sps_ogc_processes_api.models.inline_or_ref_data import InlineOrRefData
from unity_sps_ogc_processes_api.models.job_list import JobList
from unity_sps_ogc_processes_api.models.status_info import StatusInfo


class BaseJobsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseJobsApi.subclasses = BaseJobsApi.subclasses + (cls,)

    def dismiss(
        self,
        jobId: str,
    ) -> StatusInfo:
        """Cancel a job execution and remove it from the jobs list.  For more information, see [Section 14]https://docs.ogc.org/is/18-062r2/18-062r2.html#Dismiss)."""
        ...

    def get_jobs(
        self,
    ) -> JobList:
        """Lists available jobs.  For more information, see [Section 12](https://docs.ogc.org/is/18-062r2/18-062r2.html#Job_list)."""
        ...

    def get_result(
        self,
        jobId: str,
        prefer: str,
    ) -> Dict[str, InlineOrRefData]:
        """Lists available results of a job. In case of a failure, lists exceptions instead.  For more information, see [Section 7.11](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_retrieve_job_results)."""
        ...

    def get_status(
        self,
        jobId: str,
    ) -> StatusInfo:
        """Shows the status of a job.   For more information, see [Section 7.10](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_retrieve_status_info)."""
        ...
