from sqlalchemy.orm import Session
from unity_sps_ogc_processes_api.models.ogcapppkg import Ogcapppkg

from . import models


def create_process(db: Session, ogcapppkg: Ogcapppkg):
    db_process = models.Process(**ogcapppkg.process_description.model_dump())
    db_execution_unit = models.ExecutionUnit(**ogcapppkg.execution_unit.model_dump())
    db_ogcapppkg = models.Ogcapppkg(process=db_process, execution_unit=db_execution_unit)
    db.add(db_ogcapppkg)
    db.commit()
    db.refresh(db_ogcapppkg)
    return db_ogcapppkg


def update_process(db: Session, process_id: str, process_data: dict):
    db_process = db.query(models.Process).filter(models.Process.id == process_id).one()
    for key, value in process_data.items():
        if hasattr(db_process, key):
            setattr(db_process, key, value)
    db.commit()
    db.refresh(db_process)
    return db_process


def get_processes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Process).offset(skip).limit(limit).all()


def get_process(db: Session, process_id: str):
    return db.query(models.Process).filter(models.Process.id == process_id).one()


def delete_process(db: Session, process_id: str):
    db_process = db.query(models.Process).filter(models.Process.id == process_id).one()
    db.delete(db_process)
    db.commit()


def create_job(db: Session, job_data: dict):
    db_job = models.Job(**job_data)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update_job(db: Session, job_id: str, job_data: dict):
    db_job = db.query(models.Job).filter(models.Job.jobID == job_id).one()
    for key, value in job_data.items():
        if hasattr(db_job, key):
            setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()


def get_job(db: Session, job_id: str):
    return db.query(models.Job).filter(models.Job.jobID == job_id).one()


def get_results(db: Session, job_id: str):
    return db.query(models.Result).filter(models.Result.jobID == job_id).all()


def delete_job(db: Session, job: models.Job):
    db.delete(job)
    db.commit()
