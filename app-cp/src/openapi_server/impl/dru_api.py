from fastapi import Response, status

from unity_sps_ogc_processes_api.apis.dru_api_base import BaseDRUApi
from unity_sps_ogc_processes_api.models.ogcapppkg import Ogcapppkg


class DRUApiImpl(BaseDRUApi):
    def deploy(self, ogcapppkg: Ogcapppkg, w: str) -> Response:
        # Implement deploy logic here

        # Return a successful response with status code 201
        return Response(status_code=status.HTTP_201_CREATED)

    def replace(self, processId: str, ogcapppkg: Ogcapppkg) -> None:
        # Implement replace logic here
        pass

    def undeploy(self, processId: str) -> None:
        # Implement undeploy logic here
        pass
