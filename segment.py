"""
PHẦN B — PHÂN NGƯỠNG + HẬU XỬ LÝ (chỉ bạn B sửa file này)

Nhiệm vụ: nhận ảnh xám đã tiền xử lý, trả về mask nhị phân của tuyến tụy.

QUY ƯỚC (bắt buộc):
  - Input : ảnh xám uint8 0..255 (do preprocess trả ra)
  - Output: mask nhị phân, giá trị 0 và 1  (KHÔNG phải 0/255)

Các bước cần làm dần: threshold (global/otsu/adaptive) ->
Morphology (opening, closing) -> chọn component theo VỊ TRÍ (không lấy lớn nhất).
"""
import numpy as np


def segment(img, method="otsu"):
    # TODO (B): thay phần dưới bằng thuật toán ngưỡng + morphology thật.
    # Hiện tại làm ngưỡng đơn giản để cả nhóm ráp thử được.

    T = img.mean()                      # ngưỡng tạm = mức xám trung bình
    mask = (img > T).astype(np.uint8)   # ra 0/1 đúng quy ước
    return mask
