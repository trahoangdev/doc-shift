from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from app.core.config import settings
from app.services.jobs import mark_completed, mark_failed, mark_running


def perform_conversion(job_id: str, input_path: str, output_path: str) -> None:
    """Convert documents using LibreOffice in headless mode."""
    try:
        mark_running(job_id)
        output_path_obj = Path(output_path)
        output_dir = output_path_obj.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        convert_to = output_path_obj.suffix.lstrip(".").lower()
        if convert_to not in settings.ALLOWED_OUTPUT_FORMATS:
            raise ValueError(f"Unsupported output format: {convert_to}")

        if output_path_obj.exists():
            output_path_obj.unlink()

        cmd = [
            settings.LIBREOFFICE_BINARY,
            "--headless",
            "--convert-to",
            convert_to,
            "--outdir",
            str(output_dir),
            str(input_path),
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "LibreOffice conversion failed: "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )

        produced = output_dir / f"{Path(input_path).stem}.{convert_to}"
        if not produced.exists():
            raise RuntimeError("LibreOffice did not produce an output file.")

        if produced.resolve() != output_path_obj.resolve():
            shutil.move(str(produced), str(output_path_obj))

        mark_completed(job_id, output_path)
    except Exception as exc:  # pragma: no cover - best effort
        mark_failed(job_id, str(exc))
