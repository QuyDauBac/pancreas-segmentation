# Đồ án Computer Vision — Phân đoạn ảnh tuyến tụy

Phân đoạn tuyến tụy trên ảnh CT bằng kỹ thuật xử lý ảnh truyền thống
(ngưỡng + tiền xử lý miền không gian). **Không dùng Deep Learning làm phương pháp chính.**

Nhóm 4 người. Mỗi người đọc file đặc tả của mình: `TASK_A` / `TASK_B` / `TASK_C` / `TASK_D`.

---

## ⭐ LUẬT QUAN TRỌNG NHẤT — 2 quy ước dữ liệu (đọc trước khi code)

1. **A đưa cho B:** ảnh xám, kiểu `uint8`, giá trị `0–255`
2. **B đưa cho C/D:** mask nhị phân, giá trị `0` và `1` (KHÔNG phải 0/255)

Sai 2 cái này là ráp code sẽ lỗi. Thắc mắc hỏi trưởng nhóm trước khi tự chế.

---

## Pipeline

```
Ảnh CT (D load)  ->  preprocess (A)  ->  segment (B)  ->  đánh giá Dice/IoU (C)
                                                        ->  thực nghiệm + demo (D)
```

## Phân công 4 người (mỗi người CHỈ sửa file của mình)

| Người | File phụ trách | Việc chính | Chương báo cáo |
|---|---|---|---|
| A | `preprocess.py` | HU windowing, khử nhiễu, Histogram Equalization, ROI | C1 + 3.2–3.4 |
| B | `segment.py` | Global/Otsu/Adaptive threshold, Morphology, Connected Component | C2 (Related Works) + 3.5–3.7 |
| C (trưởng nhóm) | `evaluate.py`, `main.py` | Dice/IoU, tích hợp, ghép & định dạng báo cáo, điều phối | C4.2 + C5 + front matter |
| D | `data_loader.py`, `experiments.py`, `app.py` | Đọc dữ liệu, so sánh ngưỡng + ablation, demo Streamlit | C4.1 + C4.3 |

## Tên hàm cố định (không đổi tên, không đổi input/output)

```python
preprocess(img)              # A -> ảnh xám uint8 [0,255]
segment(img, method="otsu")  # B -> mask {0,1}
dice(pred, gt)               # C -> số thực 0..1
iou(pred, gt)                # C -> số thực 0..1
load_image(path)             # D -> (ảnh, ground_truth_mask)
```

---

## Cách làm việc với Git

`main` luôn chạy được. Không ai đẩy thẳng vào `main`.

```bash
git clone <link-repo>
git checkout -b ten            # mỗi người 1 nhánh riêng, đổi "ten"
# code xong:
git add .
git commit -m "mô tả việc vừa làm"
git push origin ten
```
Lên GitHub bấm **Compare & pull request** → **trưởng nhóm** xem, chạy thử rồi mới **Merge** vào `main`.

Lùi code lỗi: nút **Revert** trên GitHub, hoặc `git revert <mã commit>`. ❌ Đừng `git reset --hard` trên main chung.

## Chạy thử cả pipeline
```bash
python main.py
```
In ra Dice không lỗi nghĩa là các phần đang khớp.
