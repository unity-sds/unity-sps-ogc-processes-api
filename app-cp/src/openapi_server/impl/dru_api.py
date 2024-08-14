from unity_sps_ogc_processes_api.apis.dru_api_base import BaseDRUApi
from unity_sps_ogc_processes_api.models.ogcapppkg import Ogcapppkg


class DRUApiImpl(BaseDRUApi):
    def deploy(self, ogcapppkg: Ogcapppkg, w: str) -> None:
        # Implement deploy logic here
        pass

    def replace(self, processId: str, ogcapppkg: Ogcapppkg) -> None:
        # Implement replace logic here
        pass

    def undeploy(self, processId: str) -> None:
        # Implement undeploy logic here
        pass
