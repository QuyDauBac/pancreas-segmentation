"""
PHẦN B — PHÂN NGƯỠNG + HẬU XỬ LÝ (chỉ bạn B sửa file này).

Nhiệm vụ: nhận ảnh xám đã tiền xử lý, trả về mask nhị phân của tuyến tụy.

QUY ƯỚC (bắt buộc):
  - Input : ảnh xám uint8 0..255 (do preprocess trả ra)
  - Output: mask nhị phân, giá trị 0 và 1  (KHÔNG phải 0/255)

Pipeline gọn:
  threshold (global / otsu / adaptive)  ->  Morphology OPENING (xóa đốm nhỏ)

(Đã CHỐT: KHÔNG dùng connected component, KHÔNG chọn vùng lớn nhất —
 để đơn giản và dễ trả lời vấn đáp.)
"""
import cv2
import numpy as np


def segment(img, method="otsu"):
    if method == "global":
        mask = global_threshold(img)
    elif method == "otsu":
        mask = otsu_threshold(img)
    elif method == "adaptive":
        mask = adaptive_threshold(img)
    else:
        raise ValueError(f"method không hợp lệ: {method!r}")

    mask = opening(mask)
    return mask


def global_threshold(img):
    """Phân ngưỡng toàn cục lặp: T = (μ1 + μ2) / 2 đến khi hội tụ."""
    T = float(img.mean())

    while True:
        g1 = img[img > T]
        g2 = img[img <= T]

        if g1.size == 0 or g2.size == 0:
            break

        mu1 = float(g1.mean())
        mu2 = float(g2.mean())
        T_new = (mu1 + mu2) / 2.0

        if abs(T_new - T) < 1e-3:
            T = T_new
            break

        T = T_new

    return (img > T).astype(np.uint8)


def otsu_threshold(img):
    """Otsu: chọn T tối ưu (tối đa phương sai giữa 2 lớp)."""
    _, mask = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return mask.astype(np.uint8)


def adaptive_threshold(img):
    """Adaptive: mỗi vùng nhỏ có ngưỡng riêng (Gaussian local mean - C)."""
    block_size = 11
    C = 2
    local_mean = cv2.GaussianBlur(img.astype(np.float32), (block_size, block_size), 0)
    # Kẹp T >= 0: nền rất tối có thể cho ngưỡng âm (cv2.adaptiveThreshold đánh dấu sai).
    thresh = np.maximum(local_mean - C, 0)
    return (img > thresh).astype(np.uint8)


def opening(mask):
    """Morphology opening: xóa đốm trắng nhỏ lẻ trên mask."""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return opened.astype(np.uint8)


if __name__ == "__main__":
    img = np.zeros((100, 100), np.uint8)
    img[35:65, 35:65] = 200
    mask = segment(img, "global")
    print("gia tri trong mask:", np.unique(mask))  # mong doi: [0 1]
    print("so pixel duoc chon:", mask.sum())       # mong doi: ~900 (o 30x30)
