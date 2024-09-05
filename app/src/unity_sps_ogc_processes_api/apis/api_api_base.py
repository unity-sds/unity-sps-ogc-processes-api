# coding: utf-8

from typing import ClassVar, Tuple

from unity_sps_ogc_processes_api.models.enumeration import Enumeration


class BaseAPIApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAPIApi.subclasses = BaseAPIApi.subclasses + (cls,)

    def get_api(
        self,
        f: str,
    ) -> object: ...

    def get_api_processes(
        self,
        f: str,
    ) -> Enumeration: ...
