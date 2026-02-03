# Scope & Scale - Du an chuyen doi dinh dang tai lieu (Idea 2)

## 1) Scope theo giai doan
### MVP (4-6 tuan)
- Chuyen doi: DOCX ↔ PDF
- Upload/download 1 file
- Hang doi xu ly (job queue), thong bao hoan thanh
- Luu file tam thoi 7 ngay
- Log co ban + bao loi

### V1 (8-12 tuan)
- Xu ly hang loat (multi-file)
- Markdown ↔ DOCX/PDF/HTML
- Preview ket qua
- Tuy chon giu layout / chat luong
- Bao cao thong ke co ban (so job, ty le thanh cong)

### V2 (12-20 tuan)
- OCR anh/scan → DOCX/PDF
- PPTX → PDF (co notes/handout)
- He thong quyen nguoi dung / to chuc
- Webhook/API cho tich hop

## 2) Scale muc tieu
### Tai su dung (adoption)
- MVP: 50–200 nguoi dung thu nghiem
- V1: 500–2,000 nguoi dung hoat dong/thang
- V2: 5,000–20,000 nguoi dung hoat dong/thang

### Tai he thong (throughput)
- MVP: 200–500 job/ngay
- V1: 2,000–10,000 job/ngay
- V2: 20,000–100,000 job/ngay

### Kich thuoc file
- MVP: toi da 10MB/file
- V1: toi da 50MB/file
- V2: toi da 200MB/file (voi co che batch/async)

## 3) Muc tieu hieu nang
- 90% job < 30s voi file < 10MB
- OCR co the 1–3 phut tuy do phuc tap
- Ty le thanh cong > 98%

## 4) Tieu chi mo rong
- Worker tinh toan co the scale ngang theo queue
- Tach rieng dich vu OCR va convert de bao tai
- Luu tru S3-compatible, co lifecycle xoa sau 7–30 ngay

## 5) Gioi han & canh bao
- File qua lon → chuyen sang xu ly bat dong bo
- Dinh dang doc phuc tap → canh bao “co the sai lech layout”
- OCR nganh/ngoai ngu → can cau hinh bo tu dien

## 6) Gia dinh
- He thong phuc vu doi tuong doanh nghiep nho-vua
- Muc do bao mat co ban (khong PII y te)
- Chi can web app + API don gian
