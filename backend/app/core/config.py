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
    PUBLIC_BASE_URL: str = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")
    POPPLER_BIN: str = os.getenv("POPPLER_BIN", "")


def _resolve_soffice() -> str:
    if settings.LIBREOFFICE_BINARY:
        return settings.LIBREOFFICE_BINARY
    if os.name == "nt":
        candidate = Path(r"C:\Program Files\LibreOffice\program\soffice.exe")
        if candidate.exists():
            return str(candidate)
    return "soffice"


def _resolve_paths(current: Settings) -> Settings:
    base_dir = Path(__file__).resolve().parents[3]
    storage_dir = Path(current.STORAGE_DIR)
    db_path = Path(current.DB_PATH)
    if not storage_dir.is_absolute():
        storage_dir = (base_dir / storage_dir).resolve()
    if not db_path.is_absolute():
        db_path = (base_dir / db_path).resolve()
    return Settings(
        STORAGE_DIR=str(storage_dir),
        DB_PATH=str(db_path),
        ALLOWED_OUTPUT_FORMATS=current.ALLOWED_OUTPUT_FORMATS,
        LIBREOFFICE_BINARY=current.LIBREOFFICE_BINARY,
        REDIS_URL=current.REDIS_URL,
        PUBLIC_BASE_URL=current.PUBLIC_BASE_URL,
        POPPLER_BIN=current.POPPLER_BIN,
    )


settings = Settings()
settings = Settings(
    STORAGE_DIR=settings.STORAGE_DIR,
    DB_PATH=settings.DB_PATH,
    ALLOWED_OUTPUT_FORMATS=settings.ALLOWED_OUTPUT_FORMATS,
    LIBREOFFICE_BINARY=_resolve_soffice(),
    REDIS_URL=settings.REDIS_URL,
    PUBLIC_BASE_URL=settings.PUBLIC_BASE_URL,
    POPPLER_BIN=settings.POPPLER_BIN,
)
settings = _resolve_paths(settings)
