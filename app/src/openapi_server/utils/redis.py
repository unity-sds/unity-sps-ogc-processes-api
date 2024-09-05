from contextlib import contextmanager

import redis
from redis.exceptions import LockError


class RedisLock:
    def __init__(self, client=None, host="localhost", port=6379, db=0):
        if client is None:
            client = redis.Redis(host=host, port=port, db=db)
        self.client = client

    @contextmanager
    def lock(self, lock_id: str, lock_timeout: int = 10, blocking_timeout: int = 1):
        # Create a Redis lock object with the specified expiration timeout
        lock = self.client.lock(lock_id, timeout=lock_timeout)

        # Try to acquire the lock, waiting up to blocking_timeout seconds
        acquired = lock.acquire(blocking=True, blocking_timeout=blocking_timeout)
        try:
            if acquired:
                yield lock
            else:
                raise LockError(f"Could not acquire lock for ID {lock_id}")
        finally:
            if acquired:
                lock.release()
