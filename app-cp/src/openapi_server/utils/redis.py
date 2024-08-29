from contextlib import contextmanager

import redis
from redis.exceptions import LockError


class RedisLock:
    def __init__(self, client=None, host="localhost", port=6379, db=0):
        if client is None:
            client = redis.Redis(host=host, port=port, db=db)
        self.client = client

    @contextmanager
    def lock(self, lock_id, timeout=10):
        """Attempt to acquire a lock within the given timeout period."""
        lock = self.client.lock(lock_id, timeout=timeout)
        acquired = lock.acquire(blocking=True, blocking_timeout=timeout)
        try:
            if acquired:
                yield lock
            else:
                raise LockError(f"Could not acquire lock for ID {lock_id}")
        finally:
            if acquired:
                lock.release()
