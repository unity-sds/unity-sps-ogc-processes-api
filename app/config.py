from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite:///:memory:"
    ems_api_url: HttpUrl = "http://localhost:8080/api/v1"
    ems_api_auth_username: str = "username"
    ems_api_auth_password: str = "password"
    dag_catalog_directory: str = "/dag-catalog"
    registered_dags_directory: str = "/registered-dags"
