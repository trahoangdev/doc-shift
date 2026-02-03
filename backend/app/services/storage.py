from __future__ import annotations

from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings


async def save_upload(job_id: str, upload: UploadFile) -> str:
    storage_dir = Path(settings.STORAGE_DIR)
    storage_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(upload.filename or "file").suffix
    target = storage_dir / f"{job_id}_input{suffix}"

    with target.open("wb") as handle:
        while True:
            chunk = await upload.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)

    return str(target)


def build_output_path(job_id: str, output_format: str) -> str:
    storage_dir = Path(settings.STORAGE_DIR)
    storage_dir.mkdir(parents=True, exist_ok=True)
    return str(storage_dir / f"{job_id}_output.{output_format}")
