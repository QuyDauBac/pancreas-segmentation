# Việc của D — Dữ liệu + Thực nghiệm + Demo (`data_loader.py`, `experiments.py`, `app.py`)

## Mục tiêu
Lo dữ liệu cho cả nhóm, chạy thực nghiệm so sánh, và dựng demo Streamlit.

## Phần code phụ trách

### 1. `data_loader.py` — Dữ liệu (làm sớm nhất, cả nhóm đang chờ)
- Tải tập **NIH Pancreas-CT** (không cần hết, lấy **vài lát ảnh + ground truth mask** là đủ).
- Chạy `prepare_data.py` để chuyển DICOM + NIfTI ra các cặp `.npy` gọn nhẹ trong `data/`.
- **HU windowing là việc của bạn (D), nằm trong `data_loader.py`** — hàm `hu_window()`
  đã viết sẵn: cắt cửa sổ Hounsfield cho mô mềm rồi đưa ảnh HU thô về ảnh xám 0–255.
  Nhờ vậy A nhận sẵn ảnh xám, không phải đụng HU.
- Hàm `load_image(idx)` trả về **(ảnh xám uint8 0–255 đã HU windowing, mask {0,1})**.
- Bỏ ảnh mẫu (.npy) vào thư mục `data/` để cả nhóm test trên cùng bộ.

### 2. `experiments.py` — Thực nghiệm
- Chạy pipeline qua **nhiều ảnh**, tính Dice/IoU trung bình.
- **Bảng so sánh 3 ngưỡng:** Global vs Otsu vs Adaptive (Dice/IoU).
- **Ablation study:** Dice **có / không** từng bước tiền xử lý → chứng minh tiền xử lý có giá trị.
- Xuất **hình kết quả** (ảnh gốc, mask, overlay) cho báo cáo.

### 3. `app.py` — Demo Streamlit
- Upload ảnh CT → hiện ảnh gốc.
- Hiện ảnh sau từng bước tiền xử lý → sau threshold → mask cuối (overlay lên ảnh gốc).
- Hiện **Dice Score** so với ground truth.
- (Cộng điểm) cho chọn Global/Otsu/Adaptive và xem Dice thay đổi.

## Quy ước bắt buộc
- `load_image(path)` trả về ảnh + mask **cùng kích thước**, mask theo quy ước `{0,1}`.
- `app.py` gọi đúng `preprocess` → `segment` → `dice`, không tự chế logic riêng.

## Coi là XONG khi
- `load_image` đọc được ảnh thật + mask, đúng kích thước, mask `{0,1}`.
- `experiments.py` ra được bảng so sánh ngưỡng + bảng ablation + hình kết quả.
- `app.py` chạy `streamlit run app.py`, upload ảnh hiện đủ các bước + Dice.

## Viết phần báo cáo
- Mục 4.1 (Tập dữ liệu — mô tả NIH Pancreas-CT, định dạng, HU).
- Mục 4.3 (Kết quả thực nghiệm — bảng số liệu, hình, phân tích ca thất bại).

## Q&A phải trả lời được (phần của D)
- Tập dữ liệu gồm gì? DICOM / Hounsfield Unit là gì?
- Bảng so sánh cho thấy ngưỡng nào tốt hơn, vì sao?
- Ablation study chứng minh điều gì?
EOF
