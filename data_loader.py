"""
PHẦN D — Load dữ liệu cho cả nhóm.

Sau khi chạy prepare_data.py, trong data/ có các cặp:
    img_000.npy  (ảnh HU, int16)   +   mask_000.npy  (mask {0,1}, uint8)

Mọi người dùng load_image() để lấy ảnh + mask, không phải đụng DICOM/NIfTI.
"""
import numpy as np

def load_image(idx, data_dir="data"):
    """Trả về (ảnh HU, mask {0,1}) của lát số idx."""
    img = np.load(f"{data_dir}/img_{idx:03d}.npy")    # ảnh HU (int16) -> A sẽ HU-windowing
    mask = np.load(f"{data_dir}/mask_{idx:03d}.npy")  # mask {0,1}
    return img, mask


# Test nhanh: python data_loader.py  (cần đã có file trong data/)
if __name__ == "__main__":
    img, mask = load_image(0)
    print("ảnh:", img.shape, img.dtype, "| HU min/max:", img.min(), img.max())
    print("mask:", mask.shape, "| giá trị:", np.unique(mask), "| pixel tụy:", mask.sum())
