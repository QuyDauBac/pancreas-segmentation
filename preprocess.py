"""
PHẦN A — TIỀN XỬ LÝ (chỉ bạn A sửa file này).

Nhiệm vụ: nhận ẢNH XÁM (do D đưa, đã HU windowing), làm sạch nhiễu và tăng
tương phản để bước sau (B) tách tụy dễ hơn.

QUY ƯỚC (bắt buộc):
  - Input : ảnh xám uint8 0..255 (D đã lo HU windowing, A KHÔNG cần làm HU nữa)
  - Output: ảnh xám uint8 0..255

Pipeline gọn (chỉ 2 bước chính):
  khử nhiễu (Median HOẶC Gaussian, chọn MỘT) -> Histogram Equalization
  (tùy chọn) crop giữa ảnh để bớt phần thừa.
"""
import numpy as np


def preprocess(img, denoise="median"):
    # TODO (A): thay phần dưới bằng pipeline tiền xử lý thật.
    # Hiện tại chỉ đảm bảo đúng định dạng để cả nhóm ráp thử được.

    # Nếu lỡ là ảnh màu -> chuyển xám (lấy trung bình kênh) cho an toàn
    if img.ndim == 3:
        img = img.mean(axis=2)

    # Đưa về 0..255 dạng uint8 đúng quy ước
    out = np.clip(img, 0, 255).astype(np.uint8)
    return out
