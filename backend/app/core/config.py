from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    STORAGE_DIR: str = os.getenv("DOCSHIFT_STORAGE_DIR", "backend/storage")
    DB_PATH: str = os.getenv("DOCSHIFT_DB_PATH", "backend/storage/docshift.db")
    ALLOWED_OUTPUT_FORMATS: tuple[str, ...] = ("pdf", "docx")
    LIBREOFFICE_BINARY: str = os.getenv("LIBREOFFICE_BINARY", "")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def _resolve_soffice() -> str:
    if settings.LIBREOFFICE_BINARY:
        return settings.LIBREOFFICE_BINARY
    if os.name == "nt":
        candidate = Path(r"C:\Program Files\LibreOffice\program\soffice.exe")
        if candidate.exists():
            return str(candidate)
    return "soffice"


settings = Settings()
settings = Settings(
    STORAGE_DIR=settings.STORAGE_DIR,
    DB_PATH=settings.DB_PATH,
    ALLOWED_OUTPUT_FORMATS=settings.ALLOWED_OUTPUT_FORMATS,
    LIBREOFFICE_BINARY=_resolve_soffice(),
    REDIS_URL=settings.REDIS_URL,
)
