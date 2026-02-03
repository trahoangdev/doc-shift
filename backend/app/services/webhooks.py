from __future__ import annotations

import time

import httpx

from app.core.config import settings
from app.services.jobs import get_job


def _build_payload(job_id: str) -> dict:
    job = get_job(job_id)
    if job is None:
        return {}
    return {
        "job_id": job.id,
        "status": job.status,
        "output_url": (
            f"{settings.PUBLIC_BASE_URL}/api/jobs/{job.id}/download"
            if job.output_path
            else None
        ),
        "error": job.error,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat(),
    }


def send_webhook(job_id: str) -> None:
    job = get_job(job_id)
    if job is None or not job.webhook_url:
        return

    payload = _build_payload(job_id)
    attempts = [1, 5, 15]
    for delay in attempts:
        try:
            response = httpx.post(
                job.webhook_url,
                json=payload,
                timeout=10,
            )
            if 200 <= response.status_code < 300:
                return
        except Exception:
            pass
        time.sleep(delay)
