"""
CHẠY MỘT LẦN (trưởng nhóm hoặc D) — chuyển vài lát ảnh + mask từ
NIH Pancreas-CT (DICOM + NIfTI) ra file .npy gọn nhẹ bỏ vào data/.

Cần cài: pip install pydicom nibabel numpy
Cách chạy: chỉnh 3 đường dẫn bên dưới cho khớp máy bạn, rồi: python prepare_data.py
"""
import os, glob
import numpy as np
import pydicom
import nibabel as nib

# ===== CHỈNH 3 ĐƯỜNG DẪN NÀY CHO KHỚP MÁY BẠN =====
DICOM_CASE_DIR = "Pancreas-CT/PANCREAS_0001"                      # thư mục .dcm của 1 ca
LABEL_FILE     = "TCIA_pancreas_labels-02-05-2017/label0001.nii.gz"  # mask của đúng ca đó
OUT_DIR        = "data"
N_SLICES       = 5   # lấy bao nhiêu lát (sẽ chọn các lát có nhiều tụy nhất)
# ===================================================

os.makedirs(OUT_DIR, exist_ok=True)

# 1) Đọc DICOM, sắp xếp lát theo vị trí trục z
files = glob.glob(os.path.join(DICOM_CASE_DIR, "*.dcm"))
slices = [pydicom.dcmread(f) for f in files]
slices.sort(key=lambda s: float(s.ImagePositionPatient[2]))

def to_hu(s):
    """Đổi giá trị thô sang đơn vị Hounsfield (HU)."""
    img = s.pixel_array.astype(np.int16)
    intercept = float(getattr(s, "RescaleIntercept", 0))
    slope = float(getattr(s, "RescaleSlope", 1))
    return (img * slope + intercept).astype(np.int16)

volume = np.stack([to_hu(s) for s in slices], axis=0)   # (Z, H, W), giá trị HU

# 2) Đọc mask NIfTI, đưa về {0,1} và cùng trục với volume
mask = nib.load(LABEL_FILE).get_fdata()
mask = (mask > 0).astype(np.uint8)            # nhị phân 0/1
mask = np.transpose(mask, (2, 0, 1))          # (H,W,Z) -> (Z,H,W)

# ⚠️ NẾU overlay (bước kiểm tra) thấy mask KHÔNG trùng tụy, thử bật 1 trong các dòng:
# mask = mask[::-1]                 # lật thứ tự lát
# mask = np.flip(mask, axis=1)      # lật dọc
# mask = np.rot90(mask, k=1, axes=(1, 2))  # xoay 90 độ

assert volume.shape == mask.shape, f"Lệch kích thước: {volume.shape} vs {mask.shape}"

# 3) Chọn các lát có tụy (mask khác rỗng), lấy N_SLICES lát nhiều tụy nhất
areas = mask.reshape(mask.shape[0], -1).sum(axis=1)
idx = np.argsort(areas)[::-1][:N_SLICES]

# 4) Lưu từng cặp (ảnh HU + mask) ra .npy
for i in idx:
    np.save(os.path.join(OUT_DIR, f"img_{int(i):03d}.npy"),  volume[i])  # ảnh HU (int16)
    np.save(os.path.join(OUT_DIR, f"mask_{int(i):03d}.npy"), mask[i])    # mask {0,1}
    print(f"đã lưu lát {int(i):03d} — diện tích tụy: {int(areas[i])} pixel")

print("\nXong. Mở thư mục data/ kiểm tra.")
print("NHỚ chạy bước overlay 1 cặp để chắc mask nằm đúng trên tụy (xem hướng dẫn).")
