# DocShift

DocShift is a document format conversion tool focused on layout fidelity.

## Structure
- `backend/`: FastAPI API and worker stubs
- `frontend/`: React app (upload UI scaffold)

## Backend (dev)
1. Create venv and install deps: `python -m venv .venv` then `pip install -r backend/requirements.txt`
2. Run API: `uvicorn app.main:app --reload --app-dir backend`
3. Health check: `GET http://localhost:8000/health`

## Frontend (dev)
1. Install deps: `npm install`
2. Run dev server: `npm run dev`

## Notes
- Conversion uses LibreOffice headless. Install LibreOffice and ensure `soffice` is on PATH.
- Windows example: set `LIBREOFFICE_BINARY` to
  `C:\Program Files\LibreOffice\program\soffice.exe`
