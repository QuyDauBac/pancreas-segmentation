"""
PHẦN D — DEMO STREAMLIT (chỉ D sửa file này).

Chạy:  streamlit run app.py

Cho người dùng tải ảnh lên, chạy pipeline preprocess -> segment -> dice,
và xem kết quả từng bước. KHÔNG tự chế logic riêng — gọi đúng hàm của cả nhóm.
"""
import numpy as np
import streamlit as st

from preprocess import preprocess
from segment import segment
from evaluate import dice

st.title("Phân đoạn tuyến tụy trên ảnh CT")
st.caption("Đồ án Computer Vision — xử lý ảnh truyền thống (ngưỡng + tiền xử lý)")

# Cho chọn phương pháp ngưỡng
method = st.selectbox("Phương pháp ngưỡng", ["otsu", "global", "adaptive"])

# Tải ảnh xám (đã HU windowing) dạng .npy, hoặc dùng dữ liệu mẫu trong data/
file = st.file_uploader("Tải ảnh xám (.npy) lên", type=["npy"])

if file is not None:
    img = np.load(file)

    img_xl = preprocess(img)            # A
    mask = segment(img_xl, method)      # B

    col1, col2, col3 = st.columns(3)
    col1.image(img, caption="Ảnh gốc", clamp=True)
    col2.image(img_xl, caption="Sau tiền xử lý", clamp=True)
    col3.image(mask * 255, caption="Mask phân đoạn", clamp=True)

    # TODO (D): nếu có ground truth mask -> tính và hiện Dice:
    #   d = dice(mask, gt)
    #   st.metric("Dice Score", f"{d:.3f}")
    # TODO (D): vẽ overlay mask lên ảnh gốc cho trực quan.
else:
    st.info("Hãy tải một file ảnh .npy để bắt đầu.")
