from unity_sps_ogc_processes_api.apis.landing_page_api_base import BaseLandingPageApi
from unity_sps_ogc_processes_api.models.landing_page import LandingPage
from unity_sps_ogc_processes_api.models.link import Link


class LandingPageApiImpl(BaseLandingPageApi):
    def get_landing_page(self, f: str = None) -> LandingPage:
        landing_page = LandingPage(
            title="OGC API - Processes",
            description="This is the landing page for the OGC API - Processes implementation.",
            links=[
                Link(
                    href="/", rel="self", type="application/json", title="This document"
                ),
                Link(
                    href="/api",  # Assuming the API definition is at /api
                    rel="service-desc",
                    type="application/openapi+json;version=3.0",
                    title="The API definition",
                ),
                Link(
                    href="/conformance",
                    rel="http://www.opengis.net/def/rel/ogc/1.0/conformance",
                    type="application/json",
                    title="Conformance declaration",
                ),
                Link(
                    href="/processes",
                    rel="http://www.opengis.net/def/rel/ogc/1.0/processes",
                    type="application/json",
                    title="Processes metadata",
                ),
                Link(
                    href="/jobs",
                    rel="http://www.opengis.net/def/rel/ogc/1.0/job-list",
                    type="application/json",
                    title="Job monitoring",
                ),
            ],
        )

        return landing_page
