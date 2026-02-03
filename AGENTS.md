# AGENTS.md

## 1) Tong quan du an
- Ten du an: Cong cu chuyen doi dinh dang tai lieu (Idea 2)
- Muc tieu: Chuyen doi dinh dang tai lieu giu layout toi da, ho tro hang loat, va OCR khi can.
- Doi tuong: Nhan vien van phong, nhom hop dong/nhan su, ca nhan, doanh nghiep nho-vua.

## 2) Pham vi va giai doan
### MVP (4-6 tuan)
- DOCX ? PDF
- Upload/download 1 file
- Job queue + thong bao hoan thanh
- Luu file tam thoi 7 ngay
- Log co ban + bao loi

### V1 (8-12 tuan)
- Xu ly hang loat (multi-file)
- Markdown ? DOCX/PDF/HTML
- Preview ket qua
- Tuy chon giu layout / chat luong
- Thong ke co ban (so job, ty le thanh cong)

### V2 (12-20 tuan)
- OCR anh/scan ? DOCX/PDF
- PPTX ? PDF (co notes/handout)
- He thong quyen nguoi dung / to chuc
- Webhook/API tich hop

## 3) Yeu cau chuc nang (FR)
- FR1: Tai len 1 hoac nhieu file.
- FR2: Chon dinh dang dau ra.
- FR3: Chon tuy chon chuyen doi (giu layout, chat luong, nhung font).
- FR4: Chuyen doi va tai xuong ket qua.
- FR5: Hien thi tien trinh xu ly, thong bao khi xong.
- FR6: Ho tro OCR cho anh/scan, cho phep chon ngon ngu OCR.
- FR7: Luu lich su chuyen doi (toi thieu 7 ngay).

## 4) Yeu cau phi chuc nang (NFR)
- NFR1: Thoi gian xu ly < 30s voi file < 10MB trong 90% truong hop.
- NFR2: Ty le thanh cong > 98% voi dinh dang ho tro.
- NFR3: Bao mat: tu dong xoa file sau 7 ngay (MVP).
- NFR4: Ho tro trinh duyet moi nhat (Chrome/Edge/Safari/Firefox).
- NFR5: Mo rong ngang cho xu ly hang loat.

## 5) Kien truc de xuat (MVP)
- Frontend: React hoac Vue.
- Backend: FastAPI hoac NestJS.
- Convert: LibreOffice headless (DOCX?PDF), Pandoc (Markdown), Tesseract (OCR).
- Queue: Celery hoac BullMQ.
- Storage: S3-compatible.

## 6) Luong nguoi dung
1) Upload file.
2) Chon dinh dang dau ra + tuy chon (OCR/giu layout).
3) Bat dau chuyen doi.
4) Xem tien trinh va tai file ve.

## 7) KPI thanh cong
- Thoi gian xu ly trung binh.
- Ty le chuyen doi thanh cong.
- So luot chuyen doi hang tuan.
- Ty le quay lai (retention 7/30 ngay).

## 8) Rui ro & giam thieu
- Layout kem voi file phuc tap ? tuy chon “chat luong cao” voi engine khac.
- File qua lon ? gioi han dung luong + xu ly bat dong bo.
- OCR sai ? cho phep chon ngon ngu, bo tu dien/tu kho dong.

## 9) Nguyen tac lam viec (cho agent)
- Uu tien MVP: DOCX?PDF, luong don gian, queue + thong bao.
- Tranh mo rong sang chinh sua noi dung tai lieu.
- Bao toan layout o muc co ban (font, paragraph, bang, heading, danh sach).
- Neu can de xuat tech, uu tien stack da ne u trong PRD va Scope.

## 10) Tai lieu tham chieu
- PRD.md
- SCOPE_SCALE.md
- IDEAS.md