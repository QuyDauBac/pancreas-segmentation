"""
CHẠY MỘT LẦN (D) — cắt vài lát ảnh + mask từ tập NIH Pancreas-CT
ra các cặp file .npy gọn nhẹ bỏ vào data/ cho cả nhóm dùng.

GHI CHÚ: Trên máy mình, dataset ĐÃ được chuyển sẵn sang .npy rồi.
Mỗi ca là 1 khối 3D (512, 512, số_lát):
    images/0001.npy  -> ảnh CT thô, đơn vị HU (int16)
    labels/0001.npy  -> mask, chỉ gồm {0,1}
Nên ở đây mình KHÔNG cần pydicom/nibabel nữa, chỉ cần numpy.

Cách chạy: chỉnh 3 đường dẫn bên dưới cho khớp máy, rồi: python prepare_data.py
"""
import os
import numpy as np

# ===== CHỈNH 3 ĐƯỜNG DẪN NÀY CHO KHỚP MÁY BẠN =====
IMAGES_DIR = r"C:\Users\Admin\Downloads\CV\datasetCV\images"   # thư mục chứa các khối ảnh .npy
LABELS_DIR = r"C:\Users\Admin\Downloads\CV\datasetCV\labels"   # thư mục chứa các khối mask .npy
OUT_DIR    = "data"                                            # nơi lưu kết quả (trong repo)

CASES    = ["0001", "0002", "0003"]   # lấy 3 ca cho đồ án
N_SLICES = 5                          # mỗi ca lấy 5 lát có nhiều tụy nhất
# ===================================================

os.makedirs(OUT_DIR, exist_ok=True)

stt = 0   # số thứ tự để đặt tên file: img_000, img_001, ... (tránh trùng tên giữa các ca)

for case in CASES:
    # 1) Mở khối ảnh và khối mask của 1 ca
    volume = np.load(os.path.join(IMAGES_DIR, case + ".npy"))   # (512, 512, Z) - giá trị HU
    mask   = np.load(os.path.join(LABELS_DIR, case + ".npy"))   # (512, 512, Z) - giá trị 0/1

    mask = (mask > 0).astype(np.uint8)   # ép chắc chắn về {0,1}

    # ⚠️ NẾU overlay (bước kiểm tra) thấy mask KHÔNG trùng tụy, thử bật 1 trong các dòng:
    # mask   = mask[:, ::-1, :]                 # lật dọc
    # mask   = mask[:, :, ::-1]                 # lật thứ tự lát
    # volume = np.rot90(volume, k=1, axes=(0, 1)); mask = np.rot90(mask, k=1, axes=(0, 1))  # xoay 90 độ

    assert volume.shape == mask.shape, f"Ca {case} lệch kích thước: {volume.shape} vs {mask.shape}"

    # 2) Trục thứ 3 là trục lát (z). Đếm số pixel tụy của TỪNG lát.
    so_lat = volume.shape[2]
    dien_tich = [int(mask[:, :, i].sum()) for i in range(so_lat)]   # diện tích tụy mỗi lát

    # 3) Chọn N_SLICES lát có nhiều tụy nhất
    top = np.argsort(dien_tich)[::-1][:N_SLICES]   # chỉ số các lát nhiều tụy nhất

    # 4) Lưu từng cặp (ảnh HU + mask) ra .npy
    for i in top:
        anh_lat = volume[:, :, i].astype(np.int16)   # 1 lát ảnh HU
        mask_lat = mask[:, :, i].astype(np.uint8)    # 1 lát mask {0,1}
        np.save