from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from ..schemas import ogc_processes
from . import models


def create_process(db: Session, process: ogc_processes.Process):
    db_process = models.Process(**process.model_dump())
    db.add(db_process)
    db.commit()
    db.refresh(db_process)
    return db_process


def get_processes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Process).offset(skip).limit(limit).all()


def get_process(db: Session, process_id: str):
    return db.query(models.Process).filter(models.Process.id == process_id).one()


def delete_process(db: Session, process: models.Process):
    db.delete(process)
    db.commit()


def create_job(db: Session, execute: ogc_processes.Execute, job: ogc_processes.StatusInfo):
    db_job = models.Job(**execute.model_dump(mode="json"), **job.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update_job(db: Session, job: ogc_processes.StatusInfo):
    db_job = db.query(models.Job).filter(models.Job.jobID == job.jobID).one()
    for key, value in job.model_dump().items():
        if hasattr(db_job, key):
            setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()


def get_job(db: Session, job_id: UUID):
    return db.query(models.Job).filter(models.Job.jobID == job_id).one()


def get_results(db: Session, job_id: UUID):
    return db.query(models.Result).filter(models.Result.jobID == job_id).all()


def delete_job(db: Session, job: models.Job):
    db.delete(job)
    db.commit()
