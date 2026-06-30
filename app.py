"""
PHẦN D — DEMO STREAMLIT.

Chạy:  streamlit run app.py

Cho người dùng chọn một lát ảnh mẫu (hoặc tự tải .npy lên), chạy pipeline
preprocess -> segment, rồi xem từng bước + overlay + Dice.
KHÔNG tự chế logic riêng — gọi đúng hàm của cả nhóm.
"""
import glob, os
import numpy as np
import streamlit as st

from data_loader import load_image
from preprocess import preprocess
from segment import segment
from evaluate import dice


def tao_overlay(img_xam, mask, mau=(255, 0, 0), do_dam=0.45):
    """Chồng mask màu lên ảnh xám -> ảnh RGB uint8 để nhìn trực quan."""
    rgb = np.stack([img_xam] * 3, axis=-1).astype(np.float32)
    lop = np.zeros_like(rgb); lop[mask > 0] = mau
    out = np.where(mask[..., None] > 0, (1 - do_dam) * rgb + do_dam * lop, rgb)
    return out.astype(np.uint8)


def to_mau_them(rgb, mask, mau=(0, 255, 0), do_dam=0.85):
    """Tô thêm một lớp màu lên ảnh đã là RGB (vẽ tụy thật đè lên overlay dự đoán)."""
    rgb = rgb.astype(np.float32)
    lop = np.zeros_like(rgb); lop[mask > 0] = mau
    out = np.where(mask[..., None] > 0, (1 - do_dam) * rgb + do_dam * lop, rgb)
    return out.astype(np.uint8)


st.title("Phân đoạn tuyến tụy trên ảnh CT")
st.caption("Đồ án Computer Vision — xử lý ảnh truyền thống (tiền xử lý + phân ngưỡng)")

# --- Chọn phương pháp ngưỡng ---
method = st.selectbox("Phương pháp ngưỡng", ["otsu", "global", "adaptive"])

# --- Chọn nguồn ảnh: lát mẫu có sẵn HOẶC tự tải lên ---
so_lat = len(glob.glob(os.path.join("data", "img_*.npy")))
nguon = st.radio("Nguồn ảnh", ["Lát mẫu có sẵn", "Tự tải ảnh .npy lên"], horizontal=True)

img = None
gt = None

if nguon == "Lát mẫu có sẵn" and so_lat > 0:
    idx = st.slider("Chọn lát ảnh", 0, so_lat - 1, 0)
    img, gt = load_image(idx)              # ảnh xám 0..255 + tụy thật (GT)
elif nguon == "Tự tải ảnh .npy lên":
    file = st.file_uploader("Tải ảnh xám (.npy) lên", type=["npy"])
    if file is not None:
        img = np.load(file)
        if img.ndim == 3:                  # lỡ là ảnh màu -> lấy 1 kênh
            img = img[..., 0]
        img = img.astype(np.uint8)

# --- Chạy pipeline và hiển thị ---
if img is not None:
    img_xl = preprocess(img)               # A: tiền xử lý
    mask = segment(img_xl, method)         # B: phân ngưỡng

    # overlay: đỏ = dự đoán; nếu có GT thì tô thêm xanh lá = tụy thật
    overlay = tao_overlay(img, mask, mau=(255, 0, 0), do_dam=0.40)
    if gt is not None:
        overlay = to_mau_them(overlay, gt, mau=(0, 255, 0), do_dam=0.85)

    c1, c2 = st.columns(2)
    c1.image(img, caption="Ảnh CT gốc", clamp=True, use_container_width=True)
    c2.image(img_xl, caption="Sau tiền xử lý", clamp=True, use_container_width=True)

    c3, c4 = st.columns(2)
    c3.image(mask * 255, caption="Mask phân đoạn", clamp=True, use_container_width=True)
    cap = "Overlay (đỏ = dự đoán, xanh = tụy thật)" if gt is not None else "Overlay (đỏ = dự đoán)"
    c4.image(overlay, caption=cap, use_container_width=True)

    # Nếu có ground truth -> tính và hiện Dice
    if gt is not None:
        d = dice(mask, gt)
        st.metric("Dice Score", f"{d:.3f}")
        st.info(
            "Dice thấp là điều **dự kiến** với phương pháp ngưỡng: tụy có độ xám "
            "giống các cơ quan mô mềm lân cận, nên ngưỡng tô cả vùng mô mềm "
            "(màu đỏ) chứ không tách riêng được tụy (màu xanh)."
        )
else:
    st.info("Hãy chọn một lát ảnh mẫu hoặc tải một file .npy để bắt đầu.")
