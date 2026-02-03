from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict
from uuid import uuid4

from app.models.jobs import Job

_JOBS: Dict[str, Job] = {}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def create_job(source_filename: str, output_format: str) -> Job:
    job_id = uuid4().hex
    now = _utc_now()
    job = Job(
        id=job_id,
        source_filename=source_filename,
        output_format=output_format,
        status="queued",
        created_at=now,
        updated_at=now,
    )
    _JOBS[job_id] = job
    return job


def get_job(job_id: str) -> Job | None:
    return _JOBS.get(job_id)


def mark_running(job_id: str) -> None:
    job = _JOBS[job_id]
    job.status = "running"
    job.updated_at = _utc_now()


def mark_completed(job_id: str, output_path: str) -> None:
    job = _JOBS[job_id]
    job.status = "completed"
    job.output_path = output_path
    job.updated_at = _utc_now()


def mark_failed(job_id: str, error: str) -> None:
    job = _JOBS[job_id]
    job.status = "failed"
    job.error = error
    job.updated_at = _utc_now()
