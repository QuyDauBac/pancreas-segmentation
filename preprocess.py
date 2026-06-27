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
    img = ve_xam_neu_can(img)
    img = khu_nhieu(img, denoise)
    img = histogram_equalization(img)
    img = crop_giua(img)
    return img.astype(np.uint8)

def ve_xam_neu_can(img):
    if img.ndim == 3:
        img = img.mean(axis=2)
    return img.astype(np.uint8)

def khu_nhieu(img, denoise="median"):
    if denoise == "median":
        return median_filter(img)
    else:
        return gaussian_filter(img)

def median_filter(img):
    H, W = img.shape
    out = np.zeros_like(img)
    img_pad = np.pad(img, 1, mode='reflect')
    for y in range(H):
        for x in range(W):
            vung = img_pad[y:y+3, x:x+3]
            out[y, x] = np.median(vung)
    return out.astype(np.uint8)

def gaussian_filter(img):
    kernel = np.array([[1,2,1],[2,4,2],[1,2,1]], dtype=np.float32) / 16.0
    H, W = img.shape
    out = np.zeros_like(img, dtype=np.float32)
    img_pad = np.pad(img, 1, mode='reflect')
    for y in range(H):
        for x in range(W):
            vung = img_pad[y:y+3, x:x+3].astype(np.float32)
            out[y, x] = np.sum(vung * kernel)
    return np.clip(out, 0, 255).astype(np.uint8)

def histogram_equalization(img):
    H, W = img.shape
    hist = np.zeros(256, dtype=np.int64)
    for k in range(256):
        hist[k] = np.sum(img == k)
    cdf = np.zeros(256, dtype=np.int64)
    cdf[0] = hist[0]
    for k in range(1, 256):
        cdf[k] = cdf[k-1] + hist[k]
    cdf_min = 0
    for k in range(256):
        if cdf[k] > 0:
            cdf_min = cdf[k]
            break
    table = np.zeros(256, dtype=np.uint8)
    for k in range(256):
        if H * W - cdf_min == 0:
            table[k] = 0
        else:
            table[k] = int(np.clip(round((cdf[k] - cdf_min) / (H * W - cdf_min) * 255), 0, 255))
    return table[img]

def crop_giua(img, ty_le=0.6):
    H, W = img.shape
    new_H = int(H * ty_le)
    new_W = int(W * ty_le)
    y0 = (H - new_H) // 2
    x0 = (W - new_W) // 2
    return img[y0:y0+new_H, x0:x0+new_W]

if __name__ == "__main__":
    import numpy as np
    # ảnh giả: dải xám + vài đốm nhiễu trắng
    img = np.tile(np.arange(0, 256, 2, dtype=np.uint8), (128, 1))
    out = preprocess(img)
    print("kiểu:", out.dtype, "| min:", out.min(), "| max:", out.max())
    # mong đợi: kiểu uint8, min>=0, max<=255

# cd pancreas-segmentation
# python preprocess.py