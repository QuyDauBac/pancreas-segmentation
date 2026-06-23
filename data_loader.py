"""
PHẦN D — Load dữ liệu cho cả nhóm (chỉ D sửa file này).

Sau khi chạy prepare_data.py, trong data/ có các cặp:
    img_000.npy  (ảnh HU thô, int16)   +   mask_000.npy  (mask {0,1}, uint8)

Việc của D ở đây: biến ảnh HU thô thành ẢNH XÁM xem được (HU windowing),
rồi đưa cho cả nhóm. Nhờ vậy A chỉ việc nhận ảnh xám sạch, không phải đụng HU.

QUY ƯỚC ĐẦU RA của load_image:
    - ảnh : ảnh xám uint8, giá trị 0..255  (đã HU windowing)
    - mask: nhị phân {0,1}, uint8, cùng kích thước
"""
import numpy as np


def hu_window(img_hu, level=40, width=350):
    """
    HU WINDOWING — cắt cửa sổ Hounsfield cho mô mềm rồi đưa ảnh về 0..255.

    Ảnh CT lưu theo đơn vị HU: không khí ≈ -1000, nước ≈ 0, xương ≈ +1000.
    Tụy là mô mềm (HU thấp). Ta chỉ giữ dải HU quanh mô mềm, phần ngoài dải
    bị "kẹp" lại, rồi kéo dãn dải đó ra 0..255 cho tụy nổi rõ.

    level = tâm cửa sổ, width = độ rộng cửa sổ (mặc định hợp cho ổ bụng).
    """
    lo = level - width / 2.0          # cận dưới của cửa sổ
    hi = level + width / 2.0          # cận trên của cửa sổ
    img = np.clip(img_hu, lo, hi)     # kẹp giá trị về trong [lo, hi]
    img = (img - lo) / (hi - lo)      # đưa về 0..1
    return (img * 255).astype(np.uint8)   # ra ảnh xám 0..255


def load_image(idx, data_dir="data"):
    """Trả về (ảnh xám uint8 0..255, mask {0,1}) của lát số idx."""
    img_hu = np.load(f"{data_dir}/img_{idx:03d}.npy")    # ảnh HU thô (int16)
    mask = np.load(f"{data_dir}/mask_{idx:03d}.npy")     # mask {0,1}
    img = hu_window(img_hu)                               # -> ảnh xám 0..255
    return img, mask


# Test nhanh: python data_loader.py  (cần đã có file trong data/)
if __name__ == "__main__":
    img, mask = load_image(0)
    print("ảnh:", img.shape, img.dtype, "| min/max:", img.min(), img.max())
    print("mask:", mask.shape, "| giá trị:", np.unique(mask), "| pixel tụy:", mask.sum())
