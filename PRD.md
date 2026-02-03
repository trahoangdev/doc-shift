# PRD - Cong cu chuyen doi dinh dang tai lieu (Idea 2)

## 1. Tong quan
Cong cu cho phep nguoi dung tai len tai lieu (DOCX, PDF, Markdown, PPTX, hinh anh/scan) va chuyen doi sang dinh dang mong muon voi muc tieu giu layout toi da, xu ly hang loat, va ho tro OCR khi can.

## 2. Muc tieu
- Chuyen doi dinh dang nhanh, on dinh, giu layout tot.
- Ho tro nhieu luong cong viec (DOCX↔PDF, Markdown↔DOCX/PDF/HTML, PPTX→PDF, OCR anh/scan→DOCX).
- Cho phep xu ly hang loat va theo doi tien trinh.

## 3. Doi tuong nguoi dung
- Nhan vien hanh chinh/van phong.
- Nhom hop dong/nhan su.
- Nguoi dung ca nhan can chuyen doi nhanh.
- Doanh nghiep can xu ly tai lieu hang loat.

## 4. Pham vi (Scope)
### 4.1 In-scope
- Upload/download file (1 file hoac hang loat).
- Chuyen doi:
  - DOCX ↔ PDF
  - Markdown ↔ DOCX/PDF/HTML
  - PPTX → PDF (kem notes/handout)
  - Anh/scan → DOCX (OCR)
- Bao toan layout co ban: font, paragraph, bang, heading, danh sach.
- Xem truoc (preview) ket qua.
- Job queue, thong bao hoan thanh.

### 4.2 Out-of-scope (phien ban dau)
- Chinh sua noi dung trong trinh duyet.
- Dinh dang phuc tap (macro, form nhung, truong truong gan ket).
- Tu dong dich thuat.

## 5. Yeu cau chuc nang
- FR1: Tai len 1 hoac nhieu file.
- FR2: Chon dinh dang dau ra.
- FR3: Chon tuy chon chuyen doi (giu layout, chat luong, nhung font).
- FR4: Chuyen doi va tai xuong ket qua.
- FR5: Hien thi tien trinh xu ly, thong bao khi xong.
- FR6: Ho tro OCR cho anh/scan, cho phep chon ngon ngu OCR.
- FR7: Luu lich su chuyen doi (toi thieu 7 ngay).

## 6. Yeu cau phi chuc nang
- NFR1: Thoi gian xu ly < 30s voi file < 10MB trong 90% truong hop.
- NFR2: Ty le thanh cong > 98% voi dinh dang ho tro.
- NFR3: Bao mat: tu dong xoa file sau 7 ngay.
- NFR4: Ho tro trinh duyet moi nhat (Chrome/Edge/Safari/Firefox).
- NFR5: Mo rong ngang cho xu ly hang loat.

## 7. Luong nguoi dung (User Flow)
1) Upload file.
2) Chon dinh dang dau ra + tuy chon (OCR/giu layout).
3) Bat dau chuyen doi.
4) Xem tien trinh va tai file ve.

## 8. KPI thanh cong
- Thoi gian xu ly trung binh.
- Ty le chuyen doi thanh cong.
- So luot chuyen doi hang tuan.
- Ty le quay lai (retention 7/30 ngay).

## 9. Rui ro & giam thieu
- Chat luong layout kem voi file phuc tap → cung cap tuy chon “chat luong cao” voi engine khac.
- File qua lon → gioi han dung luong + xu ly bat dong bo.
- OCR sai → cho phep chon ngon ngu, bo tu dien/tu kho dong.

## 10. Kien truc de xuat (MVP)
- Frontend: React / Vue.
- Backend: FastAPI hoac NestJS.
- Convert: LibreOffice headless (DOCX↔PDF), Pandoc (Markdown↔DOCX/PDF), Tesseract (OCR).
- Queue: Celery/BullMQ.
- Storage: S3-compatible.

## 11. Lo trinh (MVP)
- Thang 1: DOCX↔PDF + upload/download + job queue.
- Thang 2: Markdown pipeline + OCR.
- Thang 3: PPTX→PDF + preview.
