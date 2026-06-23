"""
KIEM TRA OVERLAY — chong mask (mau do, mo) len anh xam de mat thuong
xem mask co nam DUNG tren vung tuy khong.

Cach chay: python check_overlay.py
Se mo cua so hinh (va luu file overlay_check.png).
"""
import numpy as np
import matplotlib.pyplot as plt
from data_loader import load_image   # dung dung ham cua nhom, khong tu che

# Xem 3 cap dau (moi ca 1 lat) cho de nhin
indices = [0, 5, 10]

fig, axes = plt.subplots(1, len(indices), figsize=(12, 4))
for ax, idx in zip(axes, indices):
    img, mask = load_image(idx)        # anh xam 0..255, mask {0,1}
    ax.imshow(img, cmap="gray")        # ve anh xam lam nen
    # chong mask do mo len: chi to do o cho mask = 1
    ax.imshow(np.ma.masked_where(mask == 0, mask), cmap="autumn", alpha=0.4)
    ax.set_title(f"img_{idx:03d}  (tuy = {int(mask.sum())} px)")
    ax.axis("off")

plt.tight_layout()
plt.savefig("overlay_check.png", dpi=110)
print("Da luu overlay_check.png — mo ra xem mask do co trum dung vung tuy khong.")
