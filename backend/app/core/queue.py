from __future__ import annotations

from redis import Redis
from rq import Queue

from app.core.config import settings


def get_redis() -> Redis:
    return Redis.from_url(settings.REDIS_URL)


def get_queue() -> Queue:
    # Disable job timeouts for Windows compatibility (no SIGALRM).
    return Queue("docshift", connection=get_redis(), default_timeout=None)
