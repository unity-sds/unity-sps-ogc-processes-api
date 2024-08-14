# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from unity_sps_ogc_processes_api.models.conf_classes import ConfClasses


class BaseConformanceApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseConformanceApi.subclasses = BaseConformanceApi.subclasses + (cls,)

    def get_conformance(
        self,
        f: str,
    ) -> ConfClasses: ...
