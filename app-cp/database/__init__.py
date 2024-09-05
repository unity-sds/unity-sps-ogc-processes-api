from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .. import config

settings = config.Settings()

SQLALCHEMY_DATABASE_URL = settings.DB_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
