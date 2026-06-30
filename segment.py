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
    """Otsu tự cài: chọn ngưỡng T tối đa hóa phương sai giữa 2 lớp."""
    # 1) Histogram: đếm xem mỗi mức xám 0..255 có bao nhiêu pixel.
    hist = np.bincount(img.ravel(), minlength=256).astype(np.float64)
 
    total = img.size                       # tổng số pixel của ảnh
    # Tổng "giá trị xám" của cả ảnh = Σ (mức_xám * số_pixel_mức_đó).
    # Dùng để tính trung bình của lớp sáng mà không phải quét lại ảnh.
    sum_total = np.dot(np.arange(256), hist)
 
    w0 = 0.0      # số pixel của lớp TỐI (mức xám <= T), cộng dồn
    sum0 = 0.0    # tổng giá trị xám của lớp tối, cộng dồn
    max_var = -1.0
    best_T = 0
 
    # 2) Thử từng ngưỡng T = 0..255
    for t in range(256):
        w0 += hist[t]              # thêm các pixel có mức xám = t vào lớp tối
        if w0 == 0:                # chưa có pixel nào ở lớp tối -> bỏ qua
            continue
        w1 = total - w0            # phần còn lại là lớp SÁNG (mức xám > T)
        if w1 == 0:               # hết pixel cho lớp sáng -> dừng
            break
 
        sum0 += t * hist[t]
        mu0 = sum0 / w0                    # trung bình mức xám lớp tối
        mu1 = (sum_total - sum0) / w1      # trung bình mức xám lớp sáng
 
        # 3) Phương sai giữa 2 lớp. Công thức gọn (tương đương công thức sách):
        #    σ_b² = w0 * w1 * (mu0 - mu1)²
        #    -> 2 lớp càng đông & trung bình càng cách xa thì giá trị càng lớn.
        var_between = w0 * w1 * (mu0 - mu1) ** 2
 
        if var_between > max_var:          # giữ lại ngưỡng tốt nhất tới hiện tại
            max_var = var_between
            best_T = t
 
    # 4) Nhị phân hóa: pixel sáng hơn ngưỡng -> 1 (vật), còn lại -> 0 (nền).
    #    Trả về uint8 đúng quy ước {0,1}.
    return (img > best_T).astype(np.uint8)


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
