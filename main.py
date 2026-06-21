"""
RÁP CẢ PIPELINE: A -> B -> C (trưởng nhóm giữ file này)

Chạy:  python main.py
Nếu in ra Dice mà không lỗi -> 3 phần đang khớp nhau.

Hiện dùng ảnh giả (ô vuông sáng) để chạy được ngay khi chưa có ảnh CT thật.
Khi có dữ liệu thật, thay phần tạo ảnh giả bằng đoạn đọc ảnh CT + ground truth.
"""
import numpy as np
from preprocess import preprocess
from segment import segment
from evaluate import dice, iou


def tao_anh_gia():
    # Ảnh giả: nền tối, một ô vuông sáng ở giữa (giả lập "vùng cần tách")
    img = np.zeros((100, 100), dtype=np.uint8)
    img[35:65, 35:65] = 200
    # Ground truth đúng = ô vuông đó
    gt = np.zeros((100, 100), dtype=np.uint8)
    gt[35:65, 35:65] = 1
    return img, gt


if __name__ == "__main__":
    img, gt = tao_anh_gia()

    img_xl = preprocess(img)          # A
    mask = segment(img_xl, "otsu")    # B
    d = dice(mask, gt)                # C
    j = iou(mask, gt)

    print("Pipeline chạy OK.")
    print("Dice =", round(d, 3), "| IoU =", round(j, 3))
