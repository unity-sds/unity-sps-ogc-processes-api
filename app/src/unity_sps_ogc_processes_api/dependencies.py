from functools import lru_cache

from openapi_server.config.config import Settings
from openapi_server.database import SessionLocal
from openapi_server.utils.redis import RedisLock


@lru_cache
def get_settings():
    return Settings()


@lru_cache()
def get_redis_locking_client():
    settings = get_settings()
    return RedisLock(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
