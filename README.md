# Đồ án Computer Vision — Phân đoạn ảnh tuyến tụy

Phân đoạn tuyến tụy trên ảnh CT bằng kỹ thuật xử lý ảnh truyền thống
(ngưỡng + tiền xử lý miền không gian). **Không dùng Deep Learning làm phương pháp chính.**

---

## ⭐ LUẬT QUAN TRỌNG NHẤT — 2 quy ước dữ liệu (đọc trước khi code)

Để code 3 người ráp vào nhau được, mọi người PHẢI theo đúng 2 dòng này:

1. **A đưa cho B:** ảnh xám, kiểu `uint8`, giá trị `0–255`
2. **B đưa cho C:** mask nhị phân, giá trị `0` và `1` (KHÔNG phải 0/255)

Sai 2 cái này là ráp code sẽ lỗi. Có thắc mắc hỏi trưởng nhóm trước khi tự chế.

---

## Pipeline

```
Ảnh CT  ->  preprocess (A)  ->  segment (B)  ->  đánh giá Dice/IoU (C)
```

## Phân công & file phụ trách

| Người | File CHỈ MÌNH SỬA | Việc | Chương báo cáo |
|---|---|---|---|
| A | `preprocess.py` | HU windowing, khử nhiễu, Histogram Equalization, ROI | C1 + 3.2–3.4 + 4.1 |
| B | `segment.py` | Global/Otsu/Adaptive threshold, Morphology, Connected Component | C2 + 3.5–3.7 |
| C (trưởng nhóm) | `evaluate.py`, `main.py`, `app.py` | Dice/IoU, ablation, Streamlit UI, ghép báo cáo | C4.2–4.3 + C5 |

> **Mỗi người chỉ sửa file của mình** → không bao giờ đụng code nhau → ghép cực dễ.

## Tên hàm cố định (không đổi tên, không đổi input/output)

```python
preprocess(img)              # A -> trả ảnh xám uint8 [0,255]
segment(img, method="otsu")  # B -> trả mask {0,1}
dice(pred, gt)               # C -> trả số thực 0..1
iou(pred, gt)                # C -> trả số thực 0..1
```

---

## Cách làm việc với Git (ai cũng làm theo)

`main` là bản LUÔN chạy được. Không ai đẩy thẳng vào `main`.

```bash
# Lần đầu: tải repo về
git clone <link-repo>

# Tạo nhánh riêng của mình (làm 1 lần). Đổi "ten" thành tên bạn.
git checkout -b ten

# Mỗi lần code xong, đẩy lên NHÁNH CỦA MÌNH (không phải main)
git add .
git commit -m "mô tả việc vừa làm"
git push origin ten
```

Sau đó lên GitHub bấm **"Compare & pull request"**. **Trưởng nhóm** xem, chạy thử, rồi mới bấm **Merge** vào `main`.

Mỗi lần làm tiếp, cập nhật bản mới trước:
```bash
git checkout main && git pull
git checkout ten && git merge main
```

## Lỡ đẩy code lỗi thì lùi lại

GitHub lưu mọi phiên bản, không mất gì.
- **Dễ nhất:** lên GitHub, vào commit/PR vừa merge, bấm nút **Revert**.
- **Bằng lệnh:** `git log --oneline` (copy mã commit lỗi) → `git revert <mã>` → `git push`.
- ❌ Đừng dùng `git reset --hard` trên `main` chung.

## Chạy thử cả pipeline

```bash
python main.py
```
Nếu in ra được Dice mà không lỗi → 3 phần đang ráp khớp nhau.
