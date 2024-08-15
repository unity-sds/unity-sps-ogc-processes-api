# coding: utf-8

from typing import ClassVar, Tuple

from unity_sps_ogc_processes_api.models.ogcapppkg import Ogcapppkg


class BaseDRUApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDRUApi.subclasses = BaseDRUApi.subclasses + (cls,)

    def deploy(
        self,
        ogcapppkg: Ogcapppkg,
        w: str,
    ) -> None:
        """Deploys a process.  For more information, see [Section 6.3](http://docs.ogc.org/DRAFTS/20-044.html#_87a6983e-d060-458c-95ab-27e232e64822)."""
        ...

    def replace(
        self,
        processId: str,
        ogcapppkg: Ogcapppkg,
    ) -> None:
        """Replaces a process.  For more information, see [Section 6.4](http://docs.ogc.org/DRAFTS/20-044.html#_18582f42-ebc6-4284-9333-c089068f62b6)."""
        ...

    def undeploy(
        self,
        processId: str,
    ) -> None:
        """Undeploys a process.  For more information, see [Section 6.5](http://docs.ogc.org/DRAFTS/20-044.html#_16391f9e-538f-4a84-9710-72a6bab82842)."""
        ...
