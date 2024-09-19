# coding: utf-8

from typing import ClassVar, Tuple

from unity_sps_ogc_processes_api.models.landing_page import LandingPage


class BaseLandingPageApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseLandingPageApi.subclasses = BaseLandingPageApi.subclasses + (cls,)

    def get_landing_page(
        self,
        f: str,
    ) -> LandingPage: ...
