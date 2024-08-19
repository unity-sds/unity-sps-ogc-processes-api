from fastapi.openapi.utils import get_openapi

from unity_sps_ogc_processes_api.apis.api_api_base import BaseAPIApi


class APIApiImpl(BaseAPIApi):
    def get_api(self):
        # Placeholder implementation
        return get_openapi(
            title="OGC API - Processes",
            version="1.0.0",
            description="This is a sample OpenAPI schema for OGC API - Processes",
            routes=[],
        )
