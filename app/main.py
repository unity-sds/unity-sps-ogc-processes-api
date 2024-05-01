# generated by fastapi-codegen:
#   filename:  ogcapi-processes.yaml
#   timestamp: 2024-02-16T19:06:21+00:00

from __future__ import annotations

# from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import Body, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from .config import Settings
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
)

models.Base.metadata.create_all(bind=engine)  # Create database tables


# def create_initial_processes(db: Session):
#     # Check if data already exists
#     if db.query(models.Process).first() is None:
#         # Pre-populate the database
#         processes = [
#             models.Process(
#                 version="1.0",
#                 job_control_options={"option1": "value1"},
#                 links=[{"href": "http://example.com", "rel": "self"}],
#                 inputs={"input1": "data1"},
#                 outputs={"output1": "result1"}
#             ),
#             models.Process(
#                 version="1.1",
#                 job_control_options={"option2": "value2"},
#                 links=[{"href": "http://example.org", "rel": "self"}],
#                 inputs={"input2": "data2"},
#                 outputs={"output2": "result2"}
#             )
#         ]
#         for p in processes:
#             db_item = models.Process(**p.model_dump())
#             db.add(db_item)
#             db.commit()
#             print(p.model_dump)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     db = SessionLocal()
#     create_initial_processes(db)
#     yield
#     db.close()


app = FastAPI(
    version="1.0.0",
    title="Unity Processing API conforming to the OGC API - Processes - Part 1 standard",
    description="This document is an API definition document provided alongside the OGC API - Processes standard. The OGC API - Processes Standard specifies a processing interface to communicate over a RESTful protocol using JavaScript Object Notation (JSON) encodings. The specification allows for the wrapping of computational tasks into executable processes that can be offered by a server and be invoked by a client application.",
    contact={"name": "Placeholder", "email": "Placeholder"},
    license={"name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
    servers=[],
    # lifespan=lifespan
)


@lru_cache
def get_settings():
    return Settings()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_process_integrity(db: Session, process_id: str):
    try:
        process = crud.get_process(db, process_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Process with ID {process_id} not found")
    except MultipleResultsFound:
        raise HTTPException(
            status_code=500,
            detail=f"Multiple processes found with same ID {process_id}, data integrity error",
        )
    return process


def check_job_integrity(db: Session, job_id: str):
    try:
        job = crud.get_job(db, job_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found")
    except MultipleResultsFound:
        raise HTTPException(
            status_code=500,
            detail=f"Multiple jobs found with same ID {job_id}, data integrity error",
        )
    return job


@app.get("/", response_model=LandingPage)
async def landing_page():
    """
    ## Landing Page of this API

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


@app.get("/conformance", response_model=ConfClasses)
async def conformance_declaration():
    return ConfClasses(
        conformsTo=["http://www.opengis.net/spec/ogcapi-processes-1/1.0/conf/ogc-process-description"]
    )


@app.post("/processes", response_model=Process)
async def deploy_process(db: Session = Depends(get_db), process: Process = Body(...)):
    process = check_process_integrity(db, process.id)  # TODO needs to check if already exists
    # Verify that the process_id corresponds with a DAG ID by filename
    # Copy DAG from static PVC to deployed PVC
    # Unpause DAG
    return crud.create_process(db, process)


@app.delete("/processes/{process_id}", status_code=204)
async def undeploy_process(process_id: str, db: Session = Depends(get_db)):
    process = check_process_integrity(db, process_id)
    crud.delete_process(db, process)


@app.get("/processes", response_model=ProcessList)
async def process_list(db: Session = Depends(get_db)):
    processes = crud.get_processes(db)
    process_summaries = []
    for p in processes:
        process_summaries.append(
            ProcessSummary(id=p.id, version=p.version, jobControlOptions=p.jobControlOptions, links=p.links)
        )
    links = [
        Link(href="/processes", rel="self", type="application/json", hreflang=None, title="List of processes")
    ]
    return ProcessList(processes=process_summaries, links=links)


@app.get("/processes/{process_id}", response_model=Process)
async def process_description(process_id: str, db: Session = Depends(get_db)):
    return check_process_integrity(db, process_id)


@app.get("/jobs", response_model=JobList)
async def job_list(db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db)
    links = [Link(href="/jobs", rel="self", type="application/json", hreflang=None, title="List of jobs")]
    return JobList(jobs=jobs, links=links)


@app.post("/processes/{process_id}/execution", response_model=StatusInfo)
async def execute(process_id: str, execute: Execute = Body(...), db: Session = Depends(get_db)):
    check_process_integrity(db, process_id)
    # Verify that the process_id corresponds with a DAG ID in Airflow
    # Validate that that the inputs and outputs conform to the schemas for inputs and outputs of the process
    # # Trigger DAG
    # # job_id = str(uuid.uuid4())
    # try:
    #     check_job_integrity(db, job_id)  # TODO needs to check if already exists
    # except NoResultFound:
    # StatusInfo(
    #     jobID=job_id,
    #     processID=process_id,
    #     type=ogc_processes.Type2.process.value,
    #     status=StatusCode.running,
    # ),
    # job_status = crud.create_job(db, execute, process_id, job)
    # return job_status
    # job = crud.create_job(db, execute, process_id)
    return crud.create_job(db, execute, process_id)


@app.get("/jobs/{job_id}", response_model=StatusInfo)
async def status(job_id: str, db: Session = Depends(get_db)):
    job = check_job_integrity(db, job_id)
    return job
    # check airflow job status
    # set job to updates to Pydantic model based on airflow response
    # reflect updates in db
    # return update_job(db, job)


@app.delete("/jobs/{job_id}", response_model=StatusInfo)
async def dismiss(job_id: str, db: Session = Depends(get_db)):
    job = check_job_integrity(db, job_id)
    # Pause DAG
    # Delete DAG from deployed PVC
    crud.delete_job(db, job)
    job.status = StatusCode.dismissed
    return job


@app.get("/jobs/{job_id}/results", response_model=Results)
async def results(job_id: str, db: Session = Depends(get_db)):
    check_job_integrity(db, job_id)
    return crud.get_results(db, job_id)
