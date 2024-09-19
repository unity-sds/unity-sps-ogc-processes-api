from fastapi.openapi.utils import get_openapi

from unity_sps_ogc_processes_api.apis.api_api_base import BaseAPIApi
from unity_sps_ogc_processes_api.models.enumeration import Enumeration


class APIApiImpl(BaseAPIApi):
    def get_api(self, f: str = None):
        # Implementation for retrieving the API definition
        return get_openapi(
            title="OGC API - Processes",
            version="1.0.0",
            description="This is the OpenAPI definition for OGC API - Processes",
            routes=[],  # You may need to populate this with actual routes
        )

    def get_api_processes(self, f: str = None) -> Enumeration:
        # Implementation for retrieving the list of available processes
        # This is a placeholder implementation. You should replace this with actual process list.
        return Enumeration(
            type="enum",  # Changed from 'array' to 'enum'
            enum=["process1", "process2", "process3"],  # Example process names
            title="Available Processes",
            description="List of processes available in this API implementation",
        )
