from pydantic import HttpUrl  # , PostgresDsn, AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    airflow_api_url: HttpUrl
    db_url: str
    # pg_dsn: PostgresDsn
