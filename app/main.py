# generated by fastapi-codegen:
#   filename:  ogcapi-processes.yaml
#   timestamp: 2024-02-16T19:06:21+00:00

from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import Body, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from typing_extensions import Annotated

from . import config
from .database import SessionLocal, crud, engine, models
from .schemas.ogc_processes import (
    ConfClasses,
    Execute,
    JobList,
    LandingPage,
    Link,
    Process,
    ProcessList,
    ProcessSummary,
    Results,
    StatusCode,
    StatusInfo,
    Type2,
)

models.Base.metadata.create_all(bind=engine)  # Create database tables


def create_initial_processes(db: Session):
    # Check if data already exists
    if db.query(models.Process).first() is None:
        # Pre-populate the database
        processes = [
            Process.model_validate_json(
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
        ]
        for p in processes:
            crud.create_process(db, p)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    create_initial_processes(db)
    yield
    db.close()


app = FastAPI(
    version="1.0.0",
    title="Unity Processing API conforming to the OGC API - Processes - Part 1 standard",
    description="This document is an API definition document provided alongside the OGC API - Processes standard. The OGC API - Processes Standard specifies a processing interface to communicate over a RESTful protocol using JavaScript Object Notation (JSON) encodings. The specification allows for the wrapping of computational tasks into executable processes that can be offered by a server and be invoked by a client application.",
    # contact={"name": "Placeholder", "email": "Placeholder"},
    license={"name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
    servers=[],
    lifespan=lifespan,
)


@lru_cache
def get_settings():
    return config.Settings()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_process_integrity(db: Session, process_id: str, new_process: bool):
    process = None
    try:
        process = crud.get_process(db, process_id)
        if new_process and process is not None:
            raise ValueError
    except NoResultFound:
        if not new_process:
            raise HTTPException(status_code=404, detail=f"Process with ID {process_id} not found")
    except MultipleResultsFound:
        raise HTTPException(
            status_code=500,
            detail=f"Multiple processes found with same ID {process_id}, data integrity error",
        )
    except ValueError:
        raise HTTPException(status_code=500, detail=f"Existing process with ID {process_id} already exists")
    return process


def check_job_integrity(db: Session, job_id: str, new_job: bool):
    job = None
    try:
        job = crud.get_job(db, job_id)
        if new_job and job is not None:
            raise ValueError
    except NoResultFound:
        if not new_job:
            raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found")
    except MultipleResultsFound:
        raise HTTPException(
            status_code=500,
            detail=f"Multiple jobs found with same ID {job_id}, data integrity error",
        )
    except ValueError:
        raise HTTPException(status_code=500, detail=f"Existing job with ID {job_id} already exists")
    return job


@app.get("/", response_model=LandingPage, summary="Landing page of this API")
async def landing_page():
    """
    The landing page provides links to the:
    - API Definition (no fixed path),
    - Conformance Statements (`/conformance`),
    - Processes Metadata (`/processes`),
    - Endpoint for Job Monitoring (`/jobs`).

    For more information, see [Section 7.2](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_landing_page).
    """
    return LandingPage(
        title="Unity SPS Processing Server",
        description="Server implementing the OGC API - Processes 1.0 Standard",
        links=[Link(href="/conformance"), Link(href="/processes"), Link(href="/jobs")],
    )


@app.get(
    "/conformance",
    response_model=ConfClasses,
    summary="Information about standards that this API conforms to",
)
async def conformance_declaration():
    """
    A list of all conformance classes, specified in a standard, that the server conforms to.

    | Conformance class | URI |
    | -------- | ------- |
    | Core | http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/core |
    | OGC Process Description | http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/ogc-process-description |
    | JSON | http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/json |
    | HTML | http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/html |
    | OpenAPI | Specification 3.0	http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/oas30 |
    | Job list | http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/job-list |
    | Callback | http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/callback |
    | Dismiss |	http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/dismiss |

    For more information, see [Section 7.4](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_conformance_classes).
    """
    return ConfClasses(
        conformsTo=["http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/ogc-process-description"]
    )


@app.post("/processes", response_model=Process, summary="Register a process")
async def register_process(db: Session = Depends(get_db), process: Process = Body(...)):
    """
    Register a new process.

    **Note:** This is not an officially supported endpoint in the OGC Processes specification.
    """
    check_process_integrity(db, process.id, new_process=True)
    # Verify that the process_id corresponds with a DAG ID by filename
    # Copy DAG from static PVC to deployed PVC
    # Unpause DAG
    return crud.create_process(db, process)


@app.delete("/processes/{process_id}", status_code=204, summary="Unregister a process")
async def unregister_process(process_id: str, db: Session = Depends(get_db)):
    """
    Unregister an existing process.

    **Note:** This is not an officially supported endpoint in the OGC Processes specification.
    """
    process = check_process_integrity(db, process_id, new_process=False)
    crud.delete_process(db, process)


@app.get("/processes", response_model=ProcessList, summary="Retrieve the list of available processes")
async def process_list(db: Session = Depends(get_db)):
    """
    The list of processes contains a summary of each process the OGC API - Processes offers, including the link to a more detailed description of the process.

    For more information, see [Section 7.9](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_process_list).
    """
    processes = crud.get_processes(db)
    process_summaries = []
    for p in processes:
        process_summaries.append(ProcessSummary(**Process.model_validate(p).model_dump()))
    links = [
        Link(href="/processes", rel="self", type="application/json", hreflang=None, title="List of processes")
    ]
    return ProcessList(processes=process_summaries, links=links)


@app.get("/processes/{process_id}", response_model=Process, summary="Retrieve a process description")
async def process_description(process_id: str, db: Session = Depends(get_db)):
    """
    The process description contains information about inputs and outputs and a link to the execution-endpoint for the process. The Core does not mandate the use of a specific process description to specify the interface of a process. That said, the Core requirements class makes the following recommendation:

    Implementations SHOULD consider supporting the OGC process description.

    For more information, see [Section 7.10](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_process_description).
    """
    return check_process_integrity(db, process_id, new_process=False)


@app.get("/jobs", response_model=JobList, summary="Retrieve the list of jobs")
async def job_list(db: Session = Depends(get_db)):
    """
    Lists available jobs.

    For more information, see [Section 11](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_job_list).
    """
    jobs = crud.get_jobs(db)
    links = [Link(href="/jobs", rel="self", type="application/json", hreflang=None, title="List of jobs")]
    return JobList(jobs=jobs, links=links)


@app.post("/processes/{process_id}/execution", response_model=StatusInfo, summary="Execute a process")
async def execute(
    settings: Annotated[config.Settings, Depends(get_settings)],
    process_id: str,
    execute: Execute = Body(...),
    db: Session = Depends(get_db),
):
    """
    Create a new job.

    For more information, see [Section 7.11](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_create_job).
    """
    print(settings.airflow_api_url)
    check_process_integrity(db, process_id, new_process=False)
    # Verify that the process_id corresponds with a DAG ID in Airflow
    # Validate that that the inputs and outputs conform to the schemas for inputs and outputs of the process
    # # Trigger DAG
    job_id = str(uuid.uuid4())
    # try:
    #     check_process_integrity(db, process_id, new_process=False)
    #     raise ValueError()
    # except NoResultFound:
    #     StatusInfo(
    #         jobID=job_id,
    #         processID=process_id,
    #         type=ogc_processes.Type2.process.value,
    #         status=StatusCode.running,
    #     )
    check_job_integrity(db, job_id, new_job=True)
    job = StatusInfo(
        jobID=job_id,
        processID=process_id,
        type=Type2.process.value,
        status=StatusCode.accepted,
    )
    return crud.create_job(db, execute, job)


@app.get("/jobs/{job_id}", response_model=StatusInfo, summary="Retrieve the status of a job")
async def status(
    settings: Annotated[config.Settings, Depends(get_settings)], job_id: str, db: Session = Depends(get_db)
):
    """
    Shows the status of a job.

    For more information, see [Section 7.12](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_retrieve_status_info).
    """
    print(settings.airflow_api_url)
    job = check_job_integrity(db, job_id, new_job=False)
    return job
    # check airflow job status
    # set job to updates to Pydantic model based on airflow response
    # reflect updates in db
    # return update_job(db, job)


@app.delete(
    "/jobs/{job_id}", response_model=StatusInfo, summary="Cancel a job execution, remove a finished job"
)
async def dismiss(
    settings: Annotated[config.Settings, Depends(get_settings)], job_id: str, db: Session = Depends(get_db)
):
    """
    Cancel a job execution and remove it from the jobs list.

    For more information, see [Section 13](https://docs.ogc.org/is/18-062r2/18-062r2.html#Dismiss).
    """
    print(settings.airflow_api_url)

    job = check_job_integrity(db, job_id, new_job=False)
    # Pause DAG
    # Delete DAG from deployed PVC
    crud.delete_job(db, job)
    job.status = StatusCode.dismissed
    return job


@app.get("/jobs/{job_id}/results", response_model=Results, summary="Retrieve the result(s) of a job")
async def results(job_id: str, db: Session = Depends(get_db)):
    """
    Lists available results of a job. In case of a failure, lists exceptions instead.

    For more information, see [Section 7.13](https://docs.ogc.org/is/18-062r2/18-062r2.html#sc_retrieve_job_results).
    """
    check_job_integrity(db, job_id, new_job=False)
    return crud.get_results(db, job_id)
