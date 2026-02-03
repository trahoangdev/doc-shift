from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class Job(BaseModel):
    id: str
    source_filename: str
    output_format: str
    status: str
    created_at: datetime
    updated_at: datetime
    output_path: str | None = None
    error: str | None = None


class JobCreateResponse(BaseModel):
    job_id: str


class JobStatusResponse(BaseModel):
    id: str
    source_filename: str
    output_format: str
    status: str
    created_at: datetime
    updated_at: datetime
    output_path: str | None = None
    error: str | None = None
