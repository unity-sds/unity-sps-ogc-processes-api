from unity_sps_ogc_processes_api.apis.conformance_api_base import BaseConformanceApi
from unity_sps_ogc_processes_api.models.conf_classes import ConfClasses


class ConformanceApiImpl(BaseConformanceApi):
    def get_conformance(self):
        return ConfClasses(
            conforms_to=[
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/core",
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/ogc-process-description",
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/json",
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/job-list",
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/callback",
                "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/dismiss",
            ]
        )
