from unity_sps_ogc_processes_api.apis.health_api_base import BaseHealthApi
from unity_sps_ogc_processes_api.models.health_check import HealthCheck


class HealthApiImpl(BaseHealthApi):
    def get_health(self) -> HealthCheck:
        return HealthCheck(status="OK")
