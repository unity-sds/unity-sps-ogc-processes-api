# coding: utf-8

import pytest
from fastapi.testclient import TestClient

from unity_sps_ogc_processes_api.models.execution_unit import ExecutionUnit
from unity_sps_ogc_processes_api.models.input_description import InputDescription
from unity_sps_ogc_processes_api.models.job_control_options import JobControlOptions
from unity_sps_ogc_processes_api.models.link import Link
from unity_sps_ogc_processes_api.models.metadata import Metadata
from unity_sps_ogc_processes_api.models.metadata_one_of import MetadataOneOf
from unity_sps_ogc_processes_api.models.model_schema import ModelSchema
from unity_sps_ogc_processes_api.models.ogcapppkg import (
    Ogcapppkg,
    OgcapppkgExecutionUnit,
)
from unity_sps_ogc_processes_api.models.output_description import OutputDescription
from unity_sps_ogc_processes_api.models.process import Process
from unity_sps_ogc_processes_api.models.reference import Reference


@pytest.fixture
def sample_ogcapppkg():
    return Ogcapppkg(
        process_description=Process(
            id="example-process-id",
            version="1.0.0",
            title="Example Process Title",
            description="This process performs an example task.",
            keywords=["example", "process", "OGC"],
            metadata=[
                Metadata(
                    MetadataOneOf(
                        href="http://example.com/metadata",
                        rel="related",
                        type="application/json",
                        hreflang="en",
                        title="Example Metadata",
                    )
                )
            ],
            job_control_options=[
                JobControlOptions.SYNC_MINUS_EXECUTE,
                JobControlOptions.ASYNC_MINUS_EXECUTE,
            ],
            links=[
                Link(
                    href="http://example.com/process",
                    rel="self",
                    type="application/json",
                    hreflang="en",
                    title="Process Description",
                )
            ],
            inputs={
                "input1": InputDescription(
                    title="Input 1 Title",
                    description="Description of Input 1",
                    min_occurs=1,
                    max_occurs=1,
                    schema=ModelSchema(
                        Reference(ref="#/components/schemas/ExampleSchema")
                    ),
                    formats=[
                        {
                            "mediaType": "application/json",
                            "encoding": "UTF-8",
                            "schema": "http://json-schema.org/draft-07/schema#",
                        }
                    ],
                )
            },
            outputs={
                "output1": OutputDescription(
                    title="Output 1 Title",
                    description="Description of Output 1",
                    schema=ModelSchema(
                        actual_instance=Reference(
                            ref="#/components/schemas/ExampleSchema"
                        )
                    ),
                    formats=[
                        {
                            "mediaType": "application/json",
                            "encoding": "UTF-8",
                            "schema": "http://json-schema.org/draft-07/schema#",
                        }
                    ],
                )
            },
        ),
        execution_unit=OgcapppkgExecutionUnit(
            ExecutionUnit(
                type="docker",
                image="example/image:latest",
                deployment="cloud",
                config={
                    "cpu": "2",
                    "memory": "4GiB",
                    "env": {"EXAMPLE_ENV_VAR": "value"},
                },
            )
        ),
    )


def test_deploy(client: TestClient, sample_ogcapppkg):
    """Test case for deploy"""
    response = client.post(
        "/processes",
        json=sample_ogcapppkg.model_dump(exclude_none=True, by_alias=True),
    )
    assert response.status_code == 201


# def test_replace(client: TestClient, sample_ogcapppkg):
#     """Test case for replace"""
#     process_id = "test_process"
#     response = client.put(
#         f"/processes/{process_id}",
#         json=sample_ogcapppkg.dict(),
#     )

#     assert response.status_code == 204


# def test_undeploy(client: TestClient):
#     """Test case for undeploy"""
#     process_id = "test_process"
#     response = client.delete(f"/processes/{process_id}")

#     assert response.status_code == 204


# def test_deploy_conflict(client: TestClient, sample_ogcapppkg):
#     """Test case for deploy when process already exists"""
#     # First, deploy the process
#     client.post("/processes", json=sample_ogcapppkg.dict())

#     # Try to deploy the same process again
#     response = client.post("/processes", json=sample_ogcapppkg.dict())

#     assert response.status_code == 409
#     assert "already exists" in response.json()["detail"]


# def test_undeploy_not_found(client: TestClient):
#     """Test case for undeploy when process doesn't exist"""
#     process_id = "non_existent_process"
#     response = client.delete(f"/processes/{process_id}")

#     assert response.status_code == 404
#     assert "not found" in response.json()["detail"]
