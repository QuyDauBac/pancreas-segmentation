"""
PHẦN C — ĐÁNH GIÁ (trưởng nhóm giữ file này)

Đo chất lượng PHÂN ĐOẠN bằng cách so mask dự đoán với ground truth.
(Lưu ý: Dice/IoU đo phân đoạn; PSNR/MSE chỉ đo khử nhiễu — đừng nhầm.)

QUY ƯỚC:
  - pred, gt: mask nhị phân 0/1, cùng kích thước
  - Trả về số thực trong khoảng 0..1 (càng gần 1 càng tốt)
"""
import numpy as np


def dice(pred, gt):
    pred = (pred > 0).astype(np.uint8)   # phòng trường hợp lỡ là 0/255
    gt = (gt > 0).astype(np.uint8)
    giao = np.logical_and(pred, gt).sum()       # số pixel chung
    tong = pred.sum() + gt.sum()                # tổng pixel của 2 mask
    if tong == 0:
        return 1.0                              # cả hai đều rỗng -> coi như trùng
    return 2.0 * giao / tong


def iou(pred, gt):
    pred = (pred > 0).astype(np.uint8)
    gt = (gt > 0).astype(np.uint8)
    giao = np.logical_and(pred, gt).sum()
    hop = np.logical_or(pred, gt).sum()
    if hop == 0:
        return 1.0
    return giao / hop


# Kiểm tra nhanh hàm có đúng không (chạy: python evaluate.py)
if __name__ == "__main__":
    a = np.ones((4, 4))
    b = np.zeros((4, 4)); b[:2, :] = 1
    print("dice giống nhau (mong đợi 1.0):", dice(a, a))
    print("dice không giao (mong đợi 0.0):", dice(a, np.zeros((4, 4))))
    print("dice nửa chồng (mong đợi ~0.667):", round(dice(a, b), 3))
    print("iou nửa chồng (mong đợi 0.5):", round(iou(a, b), 3))
