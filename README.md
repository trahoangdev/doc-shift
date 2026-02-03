# DocShift

DocShift is a document format conversion tool focused on layout fidelity.

## Structure
- `backend/`: FastAPI API and worker
- `frontend/`: React app (upload UI scaffold)
- `docs/`: product and planning docs

## Backend (dev)
1. Create venv and install deps: `python -m venv .venv` then `pip install -r backend/requirements.txt`
2. Start Redis (docker): `docker compose up -d`
3. Run API: `uvicorn app.main:app --reload --app-dir backend`
4. Run worker: `python backend/worker.py`
5. Health check: `GET http://localhost:8000/health`

## Frontend (dev)
1. Install deps: `npm install`
2. Run dev server: `npm run dev`

## Notes
- Conversion uses LibreOffice headless. Install LibreOffice and ensure `soffice` is on PATH.
- Windows example: set `LIBREOFFICE_BINARY` to
  `C:\Program Files\LibreOffice\program\soffice.exe`
