# Backend

Prereqs:
- Redis running (`docker compose up -d`)
- LibreOffice installed (set `LIBREOFFICE_BINARY` if not on PATH)

Run API:
`uvicorn app.main:app --reload --app-dir backend`

Run worker:
`python backend/worker.py`

Note: On Windows the worker uses RQ SimpleWorker (no fork).
