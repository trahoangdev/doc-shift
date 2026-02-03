from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.core.config import settings
from app.models.jobs import Job, JobCreateResponse, JobStatusResponse
from app.services.jobs import create_job, get_job
from app.services.storage import save_upload, build_output_path
from app.workers.convert_worker import perform_conversion

router = APIRouter()


@router.post("/jobs", response_model=JobCreateResponse)
async def create_conversion_job(
    background_tasks: BackgroundTasks,
    output_format: str,
    file: UploadFile = File(...),
) -> JobCreateResponse:
    if output_format not in settings.ALLOWED_OUTPUT_FORMATS:
        raise HTTPException(status_code=400, detail="Unsupported output format")

    job = create_job(source_filename=file.filename, output_format=output_format)
    input_path = await save_upload(job.id, file)
    output_path = build_output_path(job.id, output_format)

    background_tasks.add_task(perform_conversion, job.id, input_path, output_path)
    return JobCreateResponse(job_id=job.id)


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
