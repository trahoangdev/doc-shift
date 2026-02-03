# DocShift - Huong dan khoi chay (chi tiet)

## 1) Yeu cau
- Windows 10/11
- Python 3.11+ (da co)
- Node.js 18+ (cho frontend)
- LibreOffice (de convert DOCX <-> PDF)
- Redis (cho queue RQ)

## 2) Cau hinh duong dan LibreOffice
Mac dinh app se tu tim:
`C:\Program Files\LibreOffice\program\soffice.exe`

Neu khac, set bien moi truong:
```powershell
$env:LIBREOFFICE_BINARY = "C:\Program Files\LibreOffice\program\soffice.exe"
```

## 3) Chay Redis
Kiem tra Redis dang chay:
```powershell
Test-NetConnection -ComputerName 127.0.0.1 -Port 6379
```

Neu chua chay:
- Cach A (Docker):
  ```powershell
  docker compose up -d
  ```
- Cach B (Redis local):
  ```powershell
  redis-server
  ```

## 4) Cai dependency (lan dau)
```powershell
cd "C:\CODE PROJECT 3\CODEX\PROJECT 01"
.\.venv\Scripts\python -m pip install -r backend\requirements.txt
```

## 5) Chay Backend API
```powershell
cd "C:\CODE PROJECT 3\CODEX\PROJECT 01"
$env:LIBREOFFICE_BINARY = "C:\Program Files\LibreOffice\program\soffice.exe"
.\.venv\Scripts\python -m uvicorn app.main:app --app-dir backend --port 8000
```
Kiem tra:
```
http://localhost:8000/health
```

## 6) Chay Worker (RQ)
Mo terminal khac:
```powershell
cd "C:\CODE PROJECT 3\CODEX\PROJECT 01"
.\.venv\Scripts\python backend\worker.py
```
Neu thay dong `Listening on docshift...` la OK.

## 7) Chay Frontend
```powershell
cd "C:\CODE PROJECT 3\CODEX\PROJECT 01\frontend"
npm install
npm run dev
```
Mo trinh duyet:
```
http://127.0.0.1:5173
```

## 8) E2E test nhanh bang curl
```powershell
cd "C:\CODE PROJECT 3\CODEX\PROJECT 01"
$job = curl.exe -s -X POST "http://127.0.0.1:8000/api/jobs?output_format=pdf" -F "file=@tmp\docs\docshift-sample.docx"
$jobId = (ConvertFrom-Json $job).job_id
$jobId
```
Sau do:
```
http://127.0.0.1:8000/api/jobs/<job_id>
http://127.0.0.1:8000/api/jobs/<job_id>/download
```

## 9) Loi thuong gap
- CORS loi: phai restart backend sau khi sua `backend/app/main.py`.
- WinError 2: chua set `LIBREOFFICE_BINARY` hoac LibreOffice chua cai.
- Worker loi SIGALRM: da fix, can restart worker sau khi pull.
- Redis loi: dam bao port 6379 dang mo va dung `REDIS_URL`.

Ghi chu:
- He thong tu dong don job cu hon 7 ngay (cleanup moi gio).
- Tuy chon chat luong/DPI/nhung font hien tai chi ap dung cho PDF output.

## 10) Webhook thong bao
Co the gui webhook khi job hoan thanh/that bai. Gui them form field:
- `webhook_url`: URL nhan POST JSON

Payload mau:
```
{
  "job_id": "...",
  "status": "completed|failed",
  "output_url": "http://localhost:8000/api/jobs/<id>/download",
  "error": null,
  "created_at": "...",
  "updated_at": "..."
}
```

Thong so:
- Retry 3 lan (1s, 5s, 15s)
- `PUBLIC_BASE_URL` co the set de tao output_url

## 11) Preview PDF
Endpoint:
- `GET /api/jobs/<id>/preview` (chi ho tro PDF)

Can Poppler (pdftoppm). Neu khong trong PATH, set:
```powershell
$env:POPPLER_BIN = "C:\poppler\Library\bin"
```

## 12) Cleanup failed jobs
- Failed jobs duoc don sau 1 ngay
- Preview PNG duoc xoa cung luc
