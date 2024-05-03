from pydantic import HttpUrl  # , PostgresDsn, AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str
    # pg_dsn: PostgresDsn
    ems_api_url: HttpUrl
    ems_api_auth_username: str
    ems_api_auth_password: str
