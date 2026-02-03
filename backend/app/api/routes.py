from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.queue import get_queue
from app.models.jobs import JobCreateResponse, JobStatusResponse
from app.services.jobs import create_job, get_job, list_jobs, mark_failed, set_input_path
from app.services.storage import save_upload, build_output_path
from app.workers.convert_worker import perform_conversion

router = APIRouter()


@router.post("/jobs", response_model=JobCreateResponse)
async def create_conversion_job(
    output_format: str = Form(...),
    keep_layout: bool = Form(True),
    quality: str = Form("standard"),
    embed_fonts: bool = Form(False),
    image_resolution: int | None = Form(None),
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
    except Exception as exc:
        mark_failed(job.id, str(exc))
        raise HTTPException(status_code=500, detail="Failed to enqueue job") from exc
    return JobCreateResponse(job_id=job.id)


@router.get("/jobs", response_model=list[JobStatusResponse])
async def list_job_history(limit: int = 50, offset: int = 0) -> list[JobStatusResponse]:
    jobs = list_jobs(limit=limit, offset=offset)
    return [JobStatusResponse(**job.dict()) for job in jobs]


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
