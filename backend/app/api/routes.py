from __future__ import annotations

import logging
import os
import shutil
import subprocess
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.queue import get_queue
from app.models.jobs import JobCreateResponse, JobStatusResponse
from app.services.jobs import (
    create_job,
    get_job,
    get_job_stats,
    list_jobs,
    mark_failed,
    set_input_path,
)
from app.services.storage import save_upload, build_output_path
from app.workers.convert_worker import perform_conversion

router = APIRouter()
logger = logging.getLogger("docshift.api")


@router.post("/jobs", response_model=JobCreateResponse)
async def create_conversion_job(
    output_format: str = Form(...),
    keep_layout: bool = Form(True),
    quality: str = Form("standard"),
    embed_fonts: bool = Form(False),
    image_resolution: int | None = Form(None),
    webhook_url: str | None = Form(None),
    file: UploadFile = File(...),
) -> JobCreateResponse:
    if output_format not in settings.ALLOWED_OUTPUT_FORMATS:
        raise HTTPException(status_code=400, detail="Unsupported output format")
    if quality not in ("standard", "high"):
        raise HTTPException(status_code=400, detail="Unsupported quality")
    if image_resolution not in (None, 150, 300):
        raise HTTPException(status_code=400, detail="Unsupported image resolution")

    job = create_job(
        source_filename=file.filename,
        output_format=output_format,
        keep_layout=keep_layout,
        quality=quality,
        embed_fonts=embed_fonts,
        image_resolution=image_resolution,
        webhook_url=webhook_url,
    )
    input_path = await save_upload(job.id, file)
    set_input_path(job.id, input_path)
    output_path = build_output_path(job.id, output_format)

    try:
        queue = get_queue()
        queue.enqueue(
            perform_conversion,
            job.id,
            input_path,
            output_path,
            keep_layout,
            quality,
            embed_fonts,
            image_resolution,
        )
        logger.info(
            "job_enqueued",
            extra={
                "job_id": job.id,
                "job_output_format": output_format,
                "job_quality": quality,
            },
        )
    except Exception as exc:
        mark_failed(job.id, str(exc))
        logger.error(
            "job_enqueue_failed",
            extra={"job_id": job.id, "job_error": str(exc)},
        )
        raise HTTPException(status_code=500, detail="Failed to enqueue job") from exc
    return JobCreateResponse(job_id=job.id)


@router.get("/jobs", response_model=list[JobStatusResponse])
async def list_job_history(limit: int = 50, offset: int = 0) -> list[JobStatusResponse]:
    jobs = list_jobs(limit=limit, offset=offset)
    return [JobStatusResponse(**job.dict()) for job in jobs]


@router.get("/stats")
async def job_stats() -> dict:
    return get_job_stats()


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str) -> JobStatusResponse:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobStatusResponse(**job.dict())


@router.get("/jobs/{job_id}/download")
async def download_result(job_id: str) -> FileResponse:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Job not completed")
    if not job.output_path:
        raise HTTPException(status_code=404, detail="Output not available")

    output_path = Path(job.output_path)
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Output file missing")

    filename = output_path.name
    return FileResponse(
        path=str(output_path),
        filename=filename,
        media_type="application/octet-stream",
    )


@router.get("/jobs/{job_id}/preview")
async def preview_result(job_id: str) -> FileResponse:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Job not completed")
    if not job.output_path:
        raise HTTPException(status_code=404, detail="Output not available")

    output_path = Path(job.output_path)
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Output file missing")
    if output_path.suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Preview only supported for PDF")

    storage_dir = Path(settings.STORAGE_DIR)
    preview_path = storage_dir / f"{job.id}_preview.png"
    if preview_path.exists():
        return FileResponse(path=str(preview_path), media_type="image/png")

    pdftoppm = _resolve_pdftoppm()
    if not pdftoppm:
        raise HTTPException(status_code=501, detail="pdftoppm not available")

    prefix = storage_dir / f"{job.id}_preview"
    cmd = [
        pdftoppm,
        "-png",
        "-f",
        "1",
        "-l",
        "1",
        str(output_path),
        str(prefix),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail="Preview generation failed")

    produced = Path(f"{prefix}-1.png")
    if produced.exists():
        shutil.move(str(produced), str(preview_path))
    if not preview_path.exists():
        raise HTTPException(status_code=500, detail="Preview not found")

    return FileResponse(path=str(preview_path), media_type="image/png")


def _resolve_pdftoppm() -> str | None:
    if settings.POPPLER_BIN:
        exe_name = "pdftoppm.exe" if os.name == "nt" else "pdftoppm"
        candidate = Path(settings.POPPLER_BIN) / exe_name
        if candidate.exists():
            return str(candidate)
    return shutil.which("pdftoppm")
