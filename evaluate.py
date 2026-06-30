"""
PHẦN C — ĐÁNH GIÁ (trưởng nhóm giữ file này)

Đo chất lượng PHÂN ĐOẠN bằng cách so mask dự đoán với ground truth.
(Lưu ý: Dice/IoU/Precision/Recall đo phân đoạn; PSNR/MSE chỉ đo khử nhiễu — đừng nhầm.)

QUY ƯỚC:
  - pred, gt: mask nhị phân 0/1, cùng kích thước
  - Trả về số thực trong khoảng 0..1 (càng gần 1 càng tốt)
  - Khi mẫu số = 0 (không có pixel nào để tính) -> quy ước trả 1.0 cho thống nhất.
    Trên dữ liệu thật mọi lát đều có tụy nên trường hợp này gần như không xảy ra;
    đây chỉ là "chốt chặn" tránh chia cho 0.
"""
import numpy as np


def _nhi_phan(pred, gt):
    """Ép cả hai về 0/1 (phòng khi lỡ là 0/255), trả về (pred, gt).
    Chốt chặn: 2 mask PHẢI cùng kích thước. Nếu lệch (vd mask bị crop sai,
    hay tụt thành 1 chiều) numpy có thể âm thầm broadcast ra số vô lý >1 mà
    không báo lỗi -> assert ở đây để bắt lỗi ngay, thay vì ra kết quả sai."""
    assert pred.shape == gt.shape, (
        f"pred va gt phai cung kich thuoc, nhung {pred.shape} != {gt.shape}")
    pred = (pred > 0).astype(np.uint8)
    gt = (gt > 0).astype(np.uint8)
    return pred, gt


def dice(pred, gt):
    pred, gt = _nhi_phan(pred, gt)
    giao = np.logical_and(pred, gt).sum()       # số pixel chung (TP)
    tong = pred.sum() + gt.sum()                # tổng pixel của 2 mask
    if tong == 0:
        return 1.0                              # cả hai đều rỗng -> coi như trùng
    return 2.0 * giao / tong


def iou(pred, gt):
    pred, gt = _nhi_phan(pred, gt)
    giao = np.logical_and(pred, gt).sum()       # TP
    hop = np.logical_or(pred, gt).sum()         # TP + FP + FN
    if hop == 0:
        return 1.0
    return giao / hop


def precision(pred, gt):
    """Trong số pixel MÌNH ĐOÁN là tụy, bao nhiêu % thật sự là tụy.
    precision = TP / (TP + FP) = giao / (tổng pixel dự đoán).
    Thấp => tô lan ra ngoài (nhiều báo nhầm)."""
    pred, gt = _nhi_phan(pred, gt)
    giao = np.logical_and(pred, gt).sum()       # TP
    du_doan = pred.sum()                         # TP + FP
    if du_doan == 0:
        return 1.0                               # không đoán gì -> không có báo nhầm
    return giao / du_doan


def recall(pred, gt):
    """Trong số pixel tụy THẬT, mình bắt được bao nhiêu %.
    recall = TP / (TP + FN) = giao / (tổng pixel tụy thật).
    Thấp => bỏ sót nhiều tụy."""
    pred, gt = _nhi_phan(pred, gt)
    giao = np.logical_and(pred, gt).sum()       # TP
    that = gt.sum()                              # TP + FN
    if that == 0:
        return 1.0
    return giao / that


# Kiểm tra nhanh hàm có đúng không (chạy: python evaluate.py)
if __name__ == "__main__":
    a = np.ones((4, 4))
    b = np.zeros((4, 4)); b[:2, :] = 1
    print("dice giống nhau (mong đợi 1.0):", dice(a, a))
    print("dice không giao (mong đợi 0.0):", dice(a, np.zeros((4, 4))))
    print("dice nửa chồng (mong đợi ~0.667):", round(dice(a, b), 3))
    print("iou nửa chồng (mong đợi 0.5):", round(iou(a, b), 3))
    print("precision nửa chồng (mong đợi 0.5):", round(precision(a, b), 3))
    print("recall nửa chồng (mong đợi 1.0):", round(recall(a, b), 3))
