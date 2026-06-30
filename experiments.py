"""
PHẦN D — THỰC NGHIỆM.

Chạy pipeline qua nhiều lát ảnh, so sánh 3 ngưỡng, làm ablation tiền xử lý,
và XUẤT HÌNH kết quả (ảnh gốc / mask / overlay) ra file PNG cho báo cáo.

Chạy:  python experiments.py
(cần đã có các cặp img_*.npy / mask_*.npy trong data/)
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
    ket_qua = {}
    for method in ["global", "otsu", "adaptive"]:
        ds, js = [], []
        for i in idxs:
            img, gt = load_image(i)
            mask = segment(preprocess(img), method)
            ds.append(dice(mask, gt))
            js.append(iou(mask, gt))
        ket_qua[method] = (np.mean(ds), np.mean(js))
        print(f"{method:9s} | Dice = {np.mean(ds):.3f} | IoU = {np.mean(js):.3f}")
    return ket_qua


def ablation_tien_xu_ly():
    """Ablation: Dice CÓ và KHÔNG tiền xử lý -> xem tiền xử lý có giá trị không."""
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


def tao_overlay(img_xam, mask, mau=(255, 0, 0), do_dam=0.45):
    """
    Chồng một mask màu lên ảnh xám -> ảnh RGB uint8 để nhìn trực quan.
    mau    : màu vùng mask (đỏ cho dự đoán, xanh lá cho ground truth).
    do_dam : độ đậm pha trộn (0 = không thấy mask, 1 = che hẳn ảnh).
    Dùng được cho cả app.py (Streamlit) lẫn xuất hình báo cáo.
    """
    rgb = np.stack([img_xam] * 3, axis=-1).astype(np.float32)   # xám -> 3 kênh
    lop = np.zeros_like(rgb); lop[mask > 0] = mau               # lớp màu ở vùng mask
    out = np.where(mask[..., None] > 0,
                   (1 - do_dam) * rgb + do_dam * lop, rgb)      # pha trộn
    return out.astype(np.uint8)


def _to_mau_len_rgb(rgb, mask, mau=(0, 255, 0), do_dam=0.85):
    """Tô thêm một lớp màu lên ảnh ĐÃ là RGB (để vẽ GT đè lên overlay dự đoán)."""
    rgb = rgb.astype(np.float32)
    lop = np.zeros_like(rgb); lop[mask > 0] = mau
    out = np.where(mask[..., None] > 0, (1 - do_dam) * rgb + do_dam * lop, rgb)
    return out.astype(np.uint8)


def xuat_hinh_ket_qua(cac_lat=(0, 5, 10), method="otsu", out_dir="figures"):
    """
    Mỗi lát lưu 1 hình gồm 4 bảng: gốc / sau tiền xử lý / mask / overlay.
    Overlay: ĐỎ = vùng ngưỡng dự đoán, XANH LÁ = tụy thật (ground truth).
    -> Thấy ngay: vùng đỏ rất lớn (cả mô mềm), tụy thật chỉ là đốm xanh nhỏ.
    """
    import matplotlib
    matplotlib.use("Agg")              # không cần màn hình, chỉ để lưu file
    import matplotlib.pyplot as plt

    os.makedirs(out_dir, exist_ok=True)
    for i in cac_lat:
        img, gt = load_image(i)
        img_xl = preprocess(img)
        mask = segment(img_xl, method)
        d = dice(mask, gt)

        ov = tao_overlay(img, mask, mau=(255, 0, 0), do_dam=0.40)    # đỏ = dự đoán
        ov = _to_mau_len_rgb(ov, gt, mau=(0, 255, 0), do_dam=0.85)   # xanh = tụy thật

        fig, ax = plt.subplots(1, 4, figsize=(16, 4))
        ax[0].imshow(img, cmap="gray");    ax[0].set_title("Anh CT goc")
        ax[1].imshow(img_xl, cmap="gray"); ax[1].set_title("Sau tien xu ly")
        ax[2].imshow(mask, cmap="gray");   ax[2].set_title(f"Mask nguong ({method})")
        ax[3].imshow(ov);                  ax[3].set_title(f"Do=du doan, Xanh=tuy that | Dice={d:.3f}")
        for a in ax:
            a.axis("off")
        plt.tight_layout()
        duong_dan = os.path.join(out_dir, f"ket_qua_lat_{i:03d}.png")
        plt.savefig(duong_dan, dpi=120, bbox_inches="tight")
        plt.close(fig)
        print(f"Đã lưu {duong_dan} (Dice={d:.3f})")


if __name__ == "__main__":
    so_sanh_3_nguong()
    ablation_tien_xu_ly()
    print()
    xuat_hinh_ket_qua()     # lưu hình vào figures/ cho báo cáo
