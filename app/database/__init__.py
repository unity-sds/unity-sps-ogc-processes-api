from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .. import config

settings = config.Settings()

SQLALCHEMY_DATABASE_URL = settings.db_url

# TODO remove check_same_thread when using pg
engine = create_engine(SQLALCHEMY_DATABASE_URL)  # , connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
