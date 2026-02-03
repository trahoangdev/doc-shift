from __future__ import annotations

import json
import logging
import threading
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.services.jobs import delete_expired_jobs, delete_failed_jobs, init_db

app = FastAPI(title="DocShift API", version="0.1.0")
app.include_router(router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    _configure_logging()
    init_db()
    _start_cleanup_thread()


def _cleanup_loop() -> None:
    while True:
        try:
            delete_expired_jobs(days=7)
            delete_failed_jobs(days=1)
        except Exception:
            pass
        time.sleep(60 * 60)


def _start_cleanup_thread() -> None:
    thread = threading.Thread(target=_cleanup_loop, daemon=True)
    thread.start()


def _configure_logging() -> None:
    logger = logging.getLogger()
    if logger.handlers:
        return
    handler = logging.StreamHandler()

    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            payload = {
                "level": record.levelname,
                "message": record.getMessage(),
                "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
                "logger": record.name,
            }
            extra = {k: v for k, v in record.__dict__.items() if k.startswith("job_")}
            if extra:
                payload.update(extra)
            if record.exc_info:
                payload["exc_info"] = self.formatException(record.exc_info)
            return json.dumps(payload, ensure_ascii=False)

    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
