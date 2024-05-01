import uuid

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from .main import app
from .schemas.ogc_processes import (
    ConfClasses,
    Execute,
    JobList,
    LandingPage,
    Process,
    ProcessList,
    Results,
    StatusCode,
    StatusInfo,
)

client = TestClient(app)


def test_get_landing_page():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    landing_page = LandingPage.model_validate(data)
    assert landing_page.title == "Unity SPS Processing Server"


def test_get_conformance_declaration():
    response = client.get("/conformance")
    assert response.status_code == 200
    data = response.json()
    conformance_declaration = ConfClasses.model_validate(data)
    assert len(conformance_declaration.conformsTo) > 0
    assert conformance_declaration.conformsTo == [
        "http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/ogc-process-description"
    ]


def test_deploy_process():
    process = Process.model_validate_json(
        """
    {
        "id": "EchoProcess",
        "title": "Echo Process",
        "description": "This process accepts and number of input and simple echoes each input as an output.",
        "version": "1.0.0",
        "jobControlOptions": [
            "async-execute",
            "sync-execute"
        ],
        "inputs": [{
            "stringInput": {
            "title": "String Literal Input Example",
            "description": "This is an example of a STRING literal input.",
            "schema": {
                "type": "string",
                "enum": [
                "Value1",
                "Value2",
                "Value3"
                ]
            }
            },
            "measureInput": {
            "title": "Numerical Value with UOM Example",
            "description": "This is an example of a NUMERIC literal with an associated unit of measure.",
            "schema": {
                "type": "object",
                "required": [
                "measurement",
                "uom"
                ],
                "properties": {
                "measurement": {
                    "type": "number"
                },
                "uom": {
                    "type": "string"
                },
                "reference": {
                    "type": "string",
                    "format": "uri"
                }
                }
            }
            },
            "dateInput": {
            "title": "Date Literal Input Example",
            "description": "This is an example of a DATE literal input.",
            "schema": {
                "type": "string",
                "format": "date-time"
            }
            },
            "doubleInput": {
            "title": "Bounded Double Literal Input Example",
            "description": "This is an example of a DOUBLE literal input that is bounded between a value greater than 0 and 10.  The default value is 5.",
            "schema": {
                "type": "number",
                "format": "double",
                "minimum": 0,
                "maximum": 10,
                "default": 5,
                "exclusiveMinimum": true
            }
            },
            "arrayInput": {
            "title": "Array Input Example",
            "description": "This is an example of a single process input that is an array of values.  In this case, the input array would be interpreted as a single value and not as individual inputs.",
            "schema": {
                "type": "array",
                "minItems": 2,
                "maxItems": 10,
                "items": {
                "type": "integer"
                }
            }
            },
            "complexObjectInput": {
            "title": "Complex Object Input Example",
            "description": "This is an example of a complex object input.",
            "schema": {
                "type": "object",
                "required": [
                "property1",
                "property5"
                ],
                "properties": {
                "property1": {
                    "type": "string"
                },
                "property2": {
                    "type": "string",
                    "format": "uri"
                },
                "property3": {
                    "type": "number"
                },
                "property4": {
                    "type": "string",
                    "format": "date-time"
                },
                "property5": {
                    "type": "boolean"
                }
                }
            }
            },
            "geometryInput": {
            "title": "Geometry input",
            "description": "This is an example of a geometry input.  In this case the geometry can be expressed as a GML of GeoJSON geometry.",
            "minOccurs": 2,
            "maxOccurs": 5,
            "schema": {
                "oneOf": [
                {
                    "type": "string",
                    "contentMediaType": "application/gml+xml; version=3.2",
                    "contentSchema": "http://schemas.opengis.net/gml/3.2.1/geometryBasic2d.xsd"
                },
                {
                    "format": "geojson-geometry"
                }
                ]
            }
            },
            "boundingBoxInput": {
            "title": "Bounding Box Input Example",
            "description": "This is an example of a BBOX literal input.",
            "schema": {
                "allOf": [
                {
                    "format": "ogc-bbox"
                },
                {
                    "$ref": "../../openapi/schemas/bbox.yaml"
                }
                ]
            }
            },
            "imagesInput": {
            "title": "Inline Images Value Input",
            "description": "This is an example of an image input.  In this case, the input is an array of up to 150 images that might, for example, be a set of tiles.  The oneOf[] conditional is used to indicate the acceptable image content types; GeoTIFF and JPEG 2000 in this case.  Each input image in the input array can be included inline in the execute request as a base64-encoded string or referenced using the link.yaml schema.  The use of a base64-encoded string is implied by the specification and does not need to be specified in the definition of the input.",
            "minOccurs": 1,
            "maxOccurs": 150,
            "schema": {
                "oneOf": [
                {
                    "type": "string",
                    "contentEncoding": "binary",
                    "contentMediaType": "image/tiff; application=geotiff"
                },
                {
                    "type": "string",
                    "contentEncoding": "binary",
                    "contentMediaType": "image/jp2"
                }
                ]
            }
            },
            "featureCollectionInput": {
            "title": "Feature Collection Input Example.",
            "description": "This is an example of an input that is a feature collection that can be encoded in one of three ways: as a GeoJSON feature collection, as a GML feature collection retrieved from a WFS or as a KML document.",
            "schema": {
                "oneOf": [
                {
                    "type": "string",
                    "contentMediaType": "application/gml+xml; version=3.2"
                },
                {
                    "type": "string",
                    "contentSchema": "https://schemas.opengis.net/kml/2.3/ogckml23.xsd",
                    "contentMediaType": "application/vnd.google-earth.kml+xml"
                },
                {
                    "allOf": [
                    {
                        "format": "geojson-feature-collection"
                    },
                    {
                        "$ref": "https://geojson.org/schema/FeatureCollection.json"
                    }
                    ]
                }
                ]
            }
            }
        }],
        "outputs": [{
            "stringOutput": {
            "schema": {
                "type": "string",
                "enum": [
                "Value1",
                "Value2",
                "Value3"
                ]
            }
            },
            "measureOutput": {
            "schema": {
                "type": "object",
                "required": [
                "measurement",
                "uom"
                ],
                "properties": {
                "measurement": {
                    "type": "number"
                },
                "uom": {
                    "type": "string"
                },
                "reference": {
                    "type": "string",
                    "format": "uri"
                }
                }
            }
            },
            "dateOutput": {
            "schema": {
                "type": "string",
                "format": "date-time"
            }
            },
            "doubleOutput": {
            "schema": {
                "type": "number",
                "format": "double",
                "minimum": 0,
                "maximum": 10,
                "default": 5,
                "exclusiveMinimum": true
            }
            },
            "arrayOutput": {
            "schema": {
                "type": "array",
                "minItems": 2,
                "maxItems": 10,
                "items": {
                "type": "integer"
                }
            }
            },
            "complexObjectOutput": {
            "schema": {
                "type": "object",
                "required": [
                "property1",
                "property5"
                ],
                "properties": {
                "property1": {
                    "type": "string"
                },
                "property2": {
                    "type": "string",
                    "format": "uri"
                },
                "property3": {
                    "type": "number"
                },
                "property4": {
                    "type": "string",
                    "format": "date-time"
                },
                "property5": {
                    "type": "boolean"
                }
                }
            }
            },
            "geometryOutput": {
            "schema": {
                "oneOf": [
                {
                    "type": "string",
                    "contentMediaType": "application/gml+xml",
                    "contentSchema": "http://schemas.opengis.net/gml/3.2.1/geometryBasic2d.xsd"
                },
                {
                    "allOf": [
                    {
                        "format": "geojson-geometry"
                    },
                    {
                        "$ref": "http://schemas.opengis.net/ogcapi/features/part1/1.0/openapi/schemas/geometryGeoJSON.yaml"
                    }
                    ]
                }
                ]
            }
            },
            "boundingBoxOutput": {
            "schema": {
                "allOf": [
                {
                    "format": "ogc-bbox"
                },
                {
                    "$ref": "../../openapi/schemas/bbox.yaml"
                }
                ]
            }
            },
            "imagesOutput": {
            "schema": {
                "oneOf": [
                {
                    "type": "string",
                    "contentEncoding": "binary",
                    "contentMediaType": "image/tiff; application=geotiff"
                },
                {
                    "type": "string",
                    "contentEncoding": "binary",
                    "contentMediaType": "image/jp2"
                }
                ]
            }
            },
            "featureCollectionOutput": {
            "schema": {
                "oneOf": [
                {
                    "type": "string",
                    "contentMediaType": "application/gml+xml; version=3.2"
                },
                {
                    "type": "string",
                    "contentMediaType": "application/vnd.google-earth.kml+xml",
                    "contentSchema": "https://schemas.opengis.net/kml/2.3/ogckml23.xsd"
                },
                {
                    "allOf": [
                    {
                        "format": "geojson-feature-collection"
                    },
                    {
                        "$ref": "https://geojson.org/schema/FeatureCollection.json"
                    }
                    ]
                }
                ]
            }
            }
        }],
        "links": [
            {
            "href": "https://processing.example.org/oapi-p/processes/EchoProcess/execution",
            "rel": "http://www.opengis.net/def/rel/ogc/1.0/execute",
            "title": "Execute endpoint"
            }
        ]
    }
    """
    )
    response = client.post("/processes", json=process.model_dump())
    assert response.status_code == 200
    data = response.json()
    process = Process.model_validate(data)
    assert process.id == "EchoProcess"


def test_get_process_list():
    response = client.get("/processes")
    assert response.status_code == 200
    data = response.json()
    assert ProcessList.model_validate(data)


def test_get_process_description():
    process_id = "EchoProcess"
    response = client.get(f"/processes/{process_id}")
    assert response.status_code == 200
    data = response.json()
    process = Process.model_validate(data)
    assert process.id == process_id


def test_get_job_list():
    response = client.get("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert JobList.model_validate(data)


def test_post_execute():
    process_id = "EchoProcess"
    execute = Execute.model_validate_json(
        """
        {
            "inputs": {
                "property1": "string",
                "property2": "string"
            },
            "outputs": {
                "property1": {
                "format": {
                    "mediaType": "string",
                    "encoding": "string",
                    "schema": "string"
                },
                "transmissionMode": "value"
                },
                "property2": {
                "format": {
                    "mediaType": "string",
                    "encoding": "string",
                    "schema": "string"
                },
                "transmissionMode": "value"
                }
            },
            "response": "raw",
            "subscriber": {
                "successUri": "http://example.com",
                "inProgressUri": "http://example.com",
                "failedUri": "http://example.com"
            }
        }
        """
    )
    response = client.post(f"/processes/{process_id}/execution", json=jsonable_encoder(execute))
    assert response.status_code == 200
    data = response.json()
    status_info = StatusInfo.model_validate(data)
    assert status_info.status == StatusCode.accepted.value
    assert status_info.processID == "EchoProcess"


def test_get_status():
    job_id = uuid.uuid4()
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    status_info = StatusInfo.model_validate(data)
    assert status_info.jobID == job_id


def test_delete_dismiss():
    job_id = uuid.uuid4()
    response = client.delete(f"/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    status_info = StatusInfo.model_validate(data)
    assert status_info.status == StatusCode.dismissed


def test_get_results():
    job_id = uuid.uuid4()
    response = client.get(f"/jobs/{job_id}/results")
    assert response.status_code == 200
    data = response.json()
    assert Results.model_validate(data)
