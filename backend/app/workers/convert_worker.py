from __future__ import annotations

import logging
import shutil
import subprocess
import time
from pathlib import Path

from app.core.config import settings
from app.services.jobs import get_job, mark_completed, mark_failed, mark_running
from app.services.webhooks import send_webhook


def perform_conversion(
    job_id: str,
    input_path: str,
    output_path: str,
    keep_layout: bool = True,
    quality: str = "standard",
    embed_fonts: bool = False,
    image_resolution: int | None = None,
) -> None:
    """Convert documents using LibreOffice in headless mode."""
    try:
        job = get_job(job_id)
        if job and job.status == "canceled":
            return
        mark_running(job_id)
        output_path_obj = Path(output_path)
        output_dir = output_path_obj.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        convert_to = output_path_obj.suffix.lstrip(".").lower()
        if convert_to not in settings.ALLOWED_OUTPUT_FORMATS:
            raise ValueError(f"Unsupported output format: {convert_to}")

        if output_path_obj.exists():
            output_path_obj.unlink()

        convert_to_arg = convert_to
        if convert_to == "pdf":
            filter_options = []
            if quality == "high":
                filter_options.append("Quality=100")
                filter_options.append("ReduceImageResolution=false")
            else:
                filter_options.append("Quality=80")
                filter_options.append("ReduceImageResolution=true")
            if image_resolution:
                filter_options.append(f"MaxImageResolution={image_resolution}")
            if embed_fonts:
                filter_options.append("EmbedStandardFonts=true")
            # keep_layout is a placeholder for future layout engines.
            _ = keep_layout
            if filter_options:
                convert_to_arg = f"pdf:writer_pdf_Export:{','.join(filter_options)}"

        cmd = [
            settings.LIBREOFFICE_BINARY,
            "--headless",
            "--convert-to",
            convert_to_arg,
            "--outdir",
            str(output_dir),
            str(input_path),
        ]

        start_ts = time.time()
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
            stem = Path(input_path).stem
            candidates = list(output_dir.glob(f"{stem}.*"))
            if convert_to == "docx":
                candidates = [
                    c
                    for c in candidates
                    if c.suffix.lower() in {".docx", ".doc", ".odt", ".rtf"}
                ]
            elif convert_to == "pdf":
                candidates = [c for c in candidates if c.suffix.lower() == ".pdf"]
            if not candidates:
                candidates = [
                    c
                    for c in output_dir.glob("*")
                    if c.is_file() and c.stat().st_mtime >= start_ts - 2
                ]
            if not candidates:
                raise RuntimeError("LibreOffice did not produce an output file.")
            produced = sorted(candidates, key=lambda p: p.stat().st_mtime)[-1]

        if convert_to == "docx" and produced.suffix.lower() in {".odt", ".rtf"}:
            intermediate = produced
            second_cmd = [
                settings.LIBREOFFICE_BINARY,
                "--headless",
                "--convert-to",
                "docx",
                "--outdir",
                str(output_dir),
                str(intermediate),
            ]
            second_result = subprocess.run(
                second_cmd,
                capture_output=True,
                text=True,
                check=False,
            )
            if second_result.returncode != 0:
                raise RuntimeError(
                    "LibreOffice docx export failed: "
                    f"{second_result.stderr.strip() or second_result.stdout.strip()}"
                )
            produced = output_dir / f"{intermediate.stem}.docx"
            if not produced.exists():
                raise RuntimeError("LibreOffice did not produce a DOCX file.")

        if produced.resolve() != output_path_obj.resolve():
            shutil.move(str(produced), str(output_path_obj))

        job = get_job(job_id)
        if job and job.status == "canceled":
            return
        mark_completed(job_id, output_path)
        logger.info("job_completed", extra={"job_id": job_id})
        send_webhook(job_id)
    except Exception as exc:  # pragma: no cover - best effort
        job = get_job(job_id)
        if job and job.status == "canceled":
            return
        mark_failed(job_id, str(exc))
        logger.error("job_failed", extra={"job_id": job_id, "job_error": str(exc)})
        send_webhook(job_id)
logger = logging.getLogger("docshift.worker")
