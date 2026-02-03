from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    STORAGE_DIR: str = os.getenv("DOCSHIFT_STORAGE_DIR", "backend/storage")
    ALLOWED_OUTPUT_FORMATS: tuple[str, ...] = ("pdf", "docx")
    LIBREOFFICE_BINARY: str = os.getenv("LIBREOFFICE_BINARY", "soffice")


settings = Settings()
