from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from . import Base


class Process(Base):
    __tablename__ = "processes"
    _id = Column(Integer, primary_key=True)
    id = Column(String, index=True, unique=True, nullable=False)
    version = Column(String)
    title = Column(String)
    description = Column(String)
    keywords = Column(JSON)
    job_control_options = Column(JSON)
    links = Column(JSON)
    inputs = Column(JSON)
    outputs = Column(JSON)
    deployment_status = Column(String, default="pending")
    jobs = relationship(
        "Job",
        back_populates="process",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    ogcapppkg = relationship(
        "Ogcapppkg",
        back_populates="process",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#appending-additional-columns-to-an-existing-declarative-mapped-class
Process.metadata = Column("metadata", JSON)


class ExecutionUnit(Base):
    __tablename__ = "execution_units"
    _id = Column(Integer, primary_key=True)
    type = Column(String)
    image = Column(String)
    deployment = Column(String)
    config = Column(JSON)
    additional_properties = Column(JSON)
    ogcapppkg_id = Column(Integer, ForeignKey("ogcapppkgs._id", ondelete="CASCADE"))
    ogcapppkg = relationship("Ogcapppkg", back_populates="execution_unit")


class Ogcapppkg(Base):
    __tablename__ = "ogcapppkgs"
    _id = Column(Integer, primary_key=True)
    process_id = Column(
        String, ForeignKey("processes.id", ondelete="CASCADE"), nullable=False
    )
    process = relationship("Process", back_populates="ogcapppkg", passive_deletes=True)
    execution_unit = relationship(
        "ExecutionUnit",
        uselist=False,
        back_populates="ogcapppkg",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Job(Base):
    __tablename__ = "jobs"
    _id = Column(Integer, primary_key=True)
    jobID = Column(String, index=True, unique=True, nullable=False)
    processID = Column(String, ForeignKey("processes.id", ondelete="CASCADE"))
    process = relationship("Process", back_populates="jobs")
    type = Column(String)
    status = Column(String)
    message = Column(String, nullable=True)
    exception = Column(JSON, nullable=True)
    created = Column(DateTime(timezone=True), default=func.now())
    started = Column(DateTime(timezone=True), nullable=True)
    finished = Column(DateTime(timezone=True), nullable=True)
    updated = Column(DateTime(timezone=True), nullable=True)
    progress = Column(Integer)
    links = Column(JSON, nullable=True)
    inputs = Column(JSON)
    outputs = Column(JSON)
    subscriber = Column(JSON)
    results = relationship(
        "Result",
        back_populates="job",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Result(Base):
    __tablename__ = "results"
    _id = Column(Integer, primary_key=True)
    jobID = Column(String, ForeignKey("jobs.jobID", ondelete="CASCADE"))
    job = relationship("Job", back_populates="results")
    root = Column(JSON)
