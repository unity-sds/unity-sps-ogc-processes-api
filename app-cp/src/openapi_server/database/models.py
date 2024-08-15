from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Process(Base):
    __tablename__ = "processes"
    _id = Column(Integer, primary_key=True)
    id = Column(String, index=True, unique=True, nullable=False)
    title = Column(String)
    description = Column(String)
    keywords = Column(JSON)
    version = Column(String)
    jobControlOptions = Column(JSON)
    links = Column(JSON)
    inputs = Column(JSON)
    outputs = Column(JSON)
    metadata = Column(JSON)
    jobs = relationship("Job", back_populates="process")


class Job(Base):
    __tablename__ = "jobs"
    _id = Column(Integer, primary_key=True)
    jobID = Column(String, index=True, unique=True, nullable=False)
    processID = Column(String, ForeignKey("processes.id"))
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
    results = relationship("Result", back_populates="job")


class Result(Base):
    __tablename__ = "results"
    _id = Column(Integer, primary_key=True)
    jobID = Column(String, ForeignKey("jobs.jobID"))
    job = relationship("Job", back_populates="results")
    root = Column(JSON)
