from __future__ import annotations

import os

from redis import Redis
from rq import Connection, Queue, SimpleWorker, Worker
from rq.timeouts import TimerDeathPenalty

from app.core.config import settings
from app.services.jobs import init_db


def run() -> None:
    init_db()
    redis_conn = Redis.from_url(settings.REDIS_URL)
    with Connection(redis_conn):
        # SimpleWorker avoids os.fork on Windows.
        worker_class = SimpleWorker if os.name == "nt" else Worker
        queue = Queue("docshift", connection=redis_conn, default_timeout=None)
        worker = worker_class([queue])
        if os.name == "nt":
            worker.death_penalty_class = TimerDeathPenalty
        worker.work()


if __name__ == "__main__":
    run()
