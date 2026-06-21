"""
PHẦN A — TIỀN XỬ LÝ (chỉ bạn A sửa file này)

Nhiệm vụ: nhận ảnh CT, trả về ảnh xám đã làm sạch & tăng tương phản.

QUY ƯỚC (bắt buộc):
  - Input : ảnh (numpy array)
  - Output: ảnh xám, kiểu uint8, giá trị 0..255

Các bước cần làm dần: HU windowing -> khử nhiễu (Median HOẶC Gaussian) ->
Histogram Equalization -> (tùy chọn) cắt ROI.
"""
import numpy as np


def preprocess(img):
    # TODO (A): thay phần dưới bằng pipeline tiền xử lý thật.
    # Hiện tại chỉ đảm bảo đúng định dạng để cả nhóm ráp thử được.

    # Nếu ảnh màu -> chuyển xám (lấy trung bình kênh) cho an toàn
    if img.ndim == 3:
        img = img.mean(axis=2)

    # Đưa về 0..255 dạng uint8 đúng quy ước
    out = np.clip(img, 0, 255).astype(np.uint8)
    return out
