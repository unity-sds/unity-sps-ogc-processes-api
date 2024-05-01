import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from ..schemas import ogc_processes
from . import models


def create_process(db: Session, process: ogc_processes.Process):
    # Copy DAG from static PVC to deployed PVC
    # Unpause DAG
    # Create new process row in processes table in DB
    db_process = models.Process(**process.model_dump(by_alias=True))
    db.add(db_process)
    db.commit()
    db.refresh(db_process)
    return db_process


def get_processes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Process).offset(skip).limit(limit).all()


def get_process(db: Session, process_id: int):
    return db.query(models.Process).filter(models.Process.id == process_id).one()


# def delete_process(db: Session, process: ogc_processes.Process):
#     # Pause DAG
#     # Delete DAG from deployed PVC
#     # Delete process from processes table in DB
#     return None


def create_job(db: Session, execute: ogc_processes.Execute, process_id: int):
    # Trigger DAG
    # Create JobStatus object and add to jobs table in DB
    # StatusInfo(
    #     jobid="job1",
    #     type=Type2.process,
    #     processid="sample-process",
    #     status=StatusCode.running,
    # ),
    job_id = str(uuid.uuid4())
    db_job = models.Job(
        jobID=job_id,
        processID=process_id,
        type=ogc_processes.Type2.process.value,
        status=ogc_processes.StatusCode.accepted.value,
        **execute.model_dump(mode="json")
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


# def update_job(db: Session, job_id: UUID):


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()


def get_job(db: Session, job_id: UUID):
    return db.query(models.Job).filter(models.Job._id == job_id).one()


def get_results(db: Session, job_id: UUID):
    return db.query(models.Result).filter(models.Result.job_id == job_id).all()


def delete_job(db: Session, job: models.Job):
    db.delete(job)
    db.commit()
