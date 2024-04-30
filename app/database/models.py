from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base


class Process(Base):
    __tablename__ = "processes"
    _id = Column(Integer, primary_key=True)
    jobs = relationship("Job", back_populates="process")

    id = Column(String, index=True, unique=True, nullable=False)
    title = Column(String)
    description = Column(String)
    keywords = Column(JSON)
    version = Column(String)
    jobcontroloptions = Column(JSON)
    links = Column(JSON)
    inputs = Column(JSON)
    outputs = Column(JSON)


# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#appending-additional-columns-to-an-existing-declarative-mapped-class
Process.metadata = Column("metadata", JSON)


class Job(Base):
    __tablename__ = "jobs"
    _id = Column(String, primary_key=True)
    process_id = Column(Integer, ForeignKey("processes._id"))
    process = relationship("Process", back_populates="jobs")
    results = relationship("Result", back_populates="job")

    type = Column(String)
    status = Column(String)
    message = Column(String, nullable=True)
    exception = Column(JSON, nullable=True)
    created = Column(DateTime(timezone=True), default=func.now())
    started = Column(DateTime(timezone=True), nullable=True)
    finished = Column(DateTime(timezone=True), nullable=True)
    updated = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    progress = Column(Integer)
    links = Column(JSON, nullable=True)


class Result(Base):
    __tablename__ = "results"
    _id = Column(Integer, primary_key=True)
    job_id = Column(String, ForeignKey("jobs._id"))
    job = relationship("Job", back_populates="results")

    root = Column(JSON)
