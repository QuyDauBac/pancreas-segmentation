"""
PHẦN D — THỰC NGHIỆM (chỉ D sửa file này).

Chạy pipeline qua nhiều lát ảnh, so sánh 3 ngưỡng, và làm ablation tiền xử lý.
Kết quả (bảng số) đưa vào báo cáo mục 4.3.

Chạy:  python experiments.py
(cần đã có các cặp img_*.npy / mask_*.npy trong data/, do prepare_data.py tạo)
"""
import glob, os
import numpy as np

from data_loader import load_image
from preprocess import preprocess
from segment import segment
from evaluate import dice, iou


def danh_sach_lat(data_dir="data"):
    """Lấy danh sách idx các lát đang có trong data/."""
    files = sorted(glob.glob(os.path.join(data_dir, "img_*.npy")))
    return [int(os.path.basename(f)[4:7]) for f in files]


def so_sanh_3_nguong():
    """Bảng so sánh Global / Otsu / Adaptive: Dice & IoU trung bình."""
    idxs = danh_sach_lat()
    print("=== So sánh 3 ngưỡng (Dice / IoU trung bình) ===")
    for method in ["global", "otsu", "adaptive"]:
        ds, js = [], []
        for i in idxs:
            img, gt = load_image(i)
            mask = segment(preprocess(img), method)
            ds.append(dice(mask, gt))
            js.append(iou(mask, gt))
        print(f"{method:9s} | Dice = {np.mean(ds):.3f} | IoU = {np.mean(js):.3f}")


def ablation_tien_xu_ly():
    """Ablation: Dice CÓ và KHÔNG tiền xử lý -> chứng minh tiền xử lý có giá trị."""
    idxs = danh_sach_lat()
    print("\n=== Ablation: ảnh hưởng của tiền xử lý (method=otsu) ===")
    for ten, dung_tien_xu_ly in [("KHÔNG tiền xử lý", False), ("CÓ tiền xử lý", True)]:
        ds = []
        for i in idxs:
            img, gt = load_image(i)
            img_vao = preprocess(img) if dung_tien_xu_ly else img
            mask = segment(img_vao, "otsu")
            ds.append(dice(mask, gt))
        print(f"{ten:18s} | Dice trung bình = {np.mean(ds):.3f}")


if __name__ == "__main__":
    so_sanh_3_nguong()
    ablation_tien_xu_ly()
    # TODO (D): xuất thêm HÌNH kết quả (ảnh gốc / mask / overlay) ra file PNG cho báo cáo.
    #           Gợi ý: dùng matplotlib, vẽ ảnh gốc + mask chồng lên, plt.savefig(...).
