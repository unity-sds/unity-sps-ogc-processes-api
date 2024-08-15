from sqlalchemy.orm import Session

from unity_sps_ogc_processes_api.models import ogcapppkg

from . import models


def create_process(db: Session, process: ogcapppkg.Ogcapppkg):
    db_process = models.Process(**process.dict())
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
