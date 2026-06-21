# Việc của C — Trưởng nhóm: Tích hợp + Đánh giá + Ghép báo cáo (`evaluate.py`, `main.py`)

## Mục tiêu
Giữ cho 3 phần ráp khớp nhau, viết hàm đo chất lượng phân đoạn, gom toàn bộ thành
báo cáo đúng chuẩn, và điều phối cả nhóm.

## Phần code phụ trách
- **`evaluate.py`** — hàm `dice(pred, gt)` và `iou(pred, gt)` (đã viết sẵn, đọc kỹ
  để hiểu từng dòng). Có thể thêm `precision`, `recall`.
- **`main.py`** — nối A → B → C, chạy thử cả pipeline (smoke test).

## Quy ước bắt buộc
- `dice(pred, gt)`, `iou(pred, gt)`: input là 2 mask `{0,1}` cùng kích thước, output số thực 0..1.
- ⚠️ **Dice/IoU đo PHÂN ĐOẠN; PSNR/MSE chỉ đo khử nhiễu — không nhầm hai cái.**

## Việc của trưởng nhóm (ngoài code)
1. **Khóa contract & quy ước** ngay từ đầu (2 quy ước dữ liệu, tên hàm) — đã làm trong README.
2. **Duyệt & merge code:** chỉ bạn merge các Pull Request vào `main`, kéo về chạy thử trước.
3. **Chạy smoke test** (`python main.py`) định kỳ để phát hiện phần nào lệch sớm.
4. **Theo dõi tiến độ** theo lịch 7 tuần, đốc thúc D lo dữ liệu sớm (vì A/B/C phụ thuộc).
5. **Ghép báo cáo cuối:** gom bài của A, B, D thành một file `.docx` đúng template:
   - Front matter: trang bìa, **bảng đánh giá mức độ hoàn thành thành viên (%)**, mục lục,
     danh mục hình/bảng.
   - Định dạng: **Times New Roman 13pt, line 1.5, canh đều, mỗi chương đầu trang mới**.
   - **Tài liệu tham khảo chuẩn IEEE**, trang mới.
6. **Tổ chức buổi khảo bài Q&A chéo** ở tuần 7.

## Viết phần báo cáo
- Mục 4.2 (Đánh giá — định nghĩa Dice/IoU/Precision/Recall).
- Chương 5 (Kết luận: 5.1 đánh giá kết quả, 5.2 ưu–nhược điểm, 5.3 hướng phát triển).
- Chịu trách nhiệm ghép + định dạng toàn bộ báo cáo.

## Coi là XONG khi
- `python evaluate.py` ra đúng: mask trùng → 1.0, không giao → 0.0, nửa chồng → dice ~0.667 / iou 0.5.
- `python main.py` chạy A→B→C ra Dice không lỗi.
- Báo cáo gom đủ 5 chương + front matter, đúng định dạng, IEEE.

## Q&A phải trả lời được (phần của C)
- Giải thích **từng dòng** hàm Dice/IoU mình viết.
- Dice/IoU và PSNR/MSE đo khác nhau thế nào?
- Toàn bộ luồng xử lý dữ liệu của chương trình (vì là trưởng nhóm, dễ bị hỏi tổng quát).
EOF
