from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "sqlite:///:memory:"
    REDIS_HOST: str = "http://localhost"
    REDIS_PORT: str = "6379"
    EMS_API_URL: HttpUrl = "http://localhost:8080/api/v1"
    EMS_API_AUTH_USERNAME: str = "username"
    EMS_API_AUTH_PASSWORD: str = "password"
    DAG_CATALOG_DIRECTORY: str = "/dag-catalog"
    DEPLOYED_DAGS_DIRECTORY: str = "/deployed-dags"
