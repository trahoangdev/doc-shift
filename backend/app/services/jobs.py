from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.core.config import settings
from app.models.jobs import Job


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _db_path() -> Path:
    path = Path(settings.DB_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                source_filename TEXT NOT NULL,
                output_format TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                output_path TEXT,
                error TEXT
            )
            """
        )


def _row_to_job(row: sqlite3.Row) -> Job:
    return Job(
        id=row["id"],
        source_filename=row["source_filename"],
        output_format=row["output_format"],
        status=row["status"],
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
        output_path=row["output_path"],
        error=row["error"],
    )


def create_job(source_filename: str, output_format: str) -> Job:
    job_id = uuid4().hex
    now = _utc_now().isoformat()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO jobs (id, source_filename, output_format, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (job_id, source_filename, output_format, "queued", now, now),
        )
    return get_job(job_id)


def get_job(job_id: str) -> Job | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if row is None:
        return None
    return _row_to_job(row)


def _update_job(job_id: str, **updates: str | None) -> None:
    if not updates:
        return
    updates["updated_at"] = _utc_now().isoformat()
    columns = ", ".join(f"{key} = ?" for key in updates.keys())
    values = list(updates.values())
    values.append(job_id)
    with _connect() as conn:
        conn.execute(f"UPDATE jobs SET {columns} WHERE id = ?", values)


def mark_running(job_id: str) -> None:
    _update_job(job_id, status="running")


def mark_completed(job_id: str, output_path: str) -> None:
    _update_job(job_id, status="completed", output_path=output_path, error=None)


def mark_failed(job_id: str, error: str) -> None:
    _update_job(job_id, status="failed", error=error)
