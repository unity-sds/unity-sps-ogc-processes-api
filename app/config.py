from pydantic import HttpUrl  # , PostgresDsn, AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite:///:memory:"
    # pg_dsn: PostgresDsn
    ems_api_url: HttpUrl = "http://localhost:8080/api/v1"
    ems_api_auth_username: str = "username"
    ems_api_auth_password: str = "password"
