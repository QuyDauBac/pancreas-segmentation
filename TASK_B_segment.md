# NHIỆM VỤ THÀNH VIÊN B — PHÂN NGƯỠNG & HẬU XỬ LÝ (`segment.py`)

> **Nếu bạn đưa file này cho một trợ lý AI:** đây là toàn bộ phần việc của thành
> viên B trong đồ án. Hãy nhờ AI giải thích từng khái niệm, hướng dẫn viết code
> từng bước theo các mục bên dưới, và kiểm tra giúp kết quả. Mọi thông tin cần
> thiết đều nằm trong file này.

---

## 1. Bối cảnh đồ án (đọc để hiểu mình đang làm gì)

Đồ án: **Phân đoạn ảnh tuyến tụy trên ảnh CT** bằng kỹ thuật xử lý ảnh truyền
thống (KHÔNG dùng Deep Learning). "Phân đoạn" nghĩa là tô ra đúng vùng tuyến tụy
trong ảnh chụp cắt lớp (CT).

Cả nhóm chia pipeline thành chuỗi 4 bước, dữ liệu chạy qua từng người:

```
D (load ảnh) -> A (tiền xử lý) -> B (PHÂN NGƯỠNG) -> C (đánh giá Dice)
```

**Bạn là B — bước phân ngưỡng.** Nhiệm vụ: từ ảnh xám đã được làm sạch (do A đưa),
tạo ra một "mask" (mặt nạ) đánh dấu đâu là vùng tuyến tụy. Bạn KHÔNG cần biết A
làm sạch ảnh thế nào — chỉ cần nhận đúng đầu vào, trả đúng đầu ra theo quy ước.

## 2. Quy ước bắt buộc (sai là cả nhóm ráp code bị lỗi)

- Bạn viết hàm tên `segment(img, method="otsu")` trong file `segment.py`.
- **Đầu vào:** ảnh xám `uint8` 0–255 (do hàm `preprocess` của A trả ra).
- **Đầu ra:** một "mask" nhị phân — mảng numpy cùng kích thước ảnh, mỗi điểm chỉ
  có giá trị `0` (không phải tụy) hoặc `1` (là tụy).

⚠️ Phải là `0` và `1`, **KHÔNG phải 0 và 255**. Đây là lỗi hay gặp nhất khi ráp code.

## 3. File `segment.py` đã có sẵn code tạm — bạn làm gì với nó?

Trong file đã có sẵn hàm `segment` **làm tạm** (chỉ cắt ngưỡng ở mức xám trung
bình) kèm dòng `# TODO (B)`. Code tạm đó chỉ để pipeline chạy thử được. **Việc của
bạn: giữ nguyên tên hàm và quy ước đầu ra `{0,1}`, thay phần ruột bên trong bằng
thuật toán thật.** Đừng đổi tên hàm `segment`.

## 4. Khái niệm "phân ngưỡng" (thresholding) cho người mới

Phân ngưỡng là chọn một giá trị T, rồi: điểm nào sáng hơn T thì cho là 1 (vật thể),
tối hơn thì cho là 0 (nền). Công thức trong slide:

```
g(x,y) = 1  nếu  f(x,y) > T
         0  nếu  f(x,y) <= T
```

Vấn đề là chọn T sao cho đúng. Bạn sẽ làm 3 cách chọn T khác nhau để so sánh.

## 5. Các bước phải làm (theo ĐÚNG thứ tự)

### Bước 1 — Phân ngưỡng (cài 3 phương pháp)

**(a) Global Threshold (ngưỡng toàn cục, lặp tự động)** — đúng thuật toán trong
slide thầy:
1. Chọn T ban đầu = mức xám trung bình của ảnh.
2. Chia ảnh theo T thành 2 nhóm: G1 (sáng hơn T) và G2 (tối hơn hoặc bằng T).
3. Tính mức xám trung bình của mỗi nhóm: μ1 và μ2.
4. Cập nhật T mới = (μ1 + μ2) / 2.
5. Lặp lại bước 2–4 đến khi T gần như không đổi nữa.

**(b) Otsu** — tự nghiên cứu thêm (slide không có). Otsu tự tìm T tối ưu bằng cách
chọn T sao cho 2 nhóm tách nhau rõ nhất. *Lưu ý: Otsu giả định ảnh có histogram 2
đỉnh (bimodal) — ảnh CT không phải lúc nào cũng vậy, cần biết để trả lời Q&A.*

**(c) Adaptive Threshold** — tự nghiên cứu thêm. Thay vì 1 ngưỡng cho cả ảnh, mỗi
vùng nhỏ có ngưỡng riêng. Hợp khi độ sáng không đều.

Hàm chọn dùng cách nào qua tham số `method` ("global" / "otsu" / "adaptive").

### Bước 2 — Morphology (hình thái học), làm sạch mask
- **Opening (mở):** xóa các đốm trắng nhỏ lẻ (nhiễu) còn sót.
- **Closing (đóng):** lấp các lỗ thủng nhỏ bên trong vùng.

### Bước 3 — Connected Component (chọn đúng vùng tụy)
Sau ngưỡng, mask có thể có nhiều mảng trắng rời rạc. Cần chọn ra mảng là tụy.

⚠️ **TUYỆT ĐỐI KHÔNG chọn mảng lớn nhất.** Tụy là cơ quan NHỎ và mờ; mảng lớn nhất
thường là gan → chọn nhầm. Hãy chọn mảng theo **vị trí** (nơi tụy thường nằm) hoặc
mảng nằm trong vùng ROI mà A đã cắt.

## 6. Gợi ý code

- Thầy yêu cầu báo cáo có **mã giả + phần tự hiện thực**, nên hãy **TỰ VIẾT** hàm
  Global Threshold lặp theo thuật toán trên (slide có sẵn). Đây là phần ghi điểm.
- Otsu / Adaptive / Morphology / Connected Component có thể dùng thư viện
  (`cv2.threshold` + cờ Otsu, `cv2.adaptiveThreshold`, `cv2.morphologyEx`,
  `cv2.connectedComponentsWithStats`) — nhưng **phải hiểu để giải thích được**.

Khung hàm sẽ phình ra đại khái như sau (viết thêm các hàm con trong cùng file):

```python
import numpy as np

def segment(img, method="otsu"):
    # 1. phân ngưỡng theo method
    if method == "global":
        mask = global_threshold(img)
    elif method == "otsu":
        mask = otsu_threshold(img)
    elif method == "adaptive":
        mask = adaptive_threshold(img)
    # 2. hậu xử lý
    mask = morphology(mask)        # opening + closing
    mask = chon_vung_tuy(mask)     # connected component theo vị trí
    return mask                    # luôn trả {0,1}

# TODO (B): viết các hàm con ở dưới
def global_threshold(img): ...     # tự cài theo thuật toán lặp
def otsu_threshold(img): ...
def morphology(mask): ...
def chon_vung_tuy(mask): ...
```

## 7. Cách tự kiểm tra phần mình (không cần chờ ai)

Thêm đoạn này vào cuối `segment.py` rồi chạy `python segment.py`:

```python
if __name__ == "__main__":
    import numpy as np
    # ảnh giả: nền tối, một ô vuông sáng ở giữa (giả lập vùng cần tách)
    img = np.zeros((100, 100), np.uint8); img[35:65, 35:65] = 200
    mask = segment(img, "global")
    print("giá trị trong mask:", np.unique(mask))  # mong đợi: [0 1]
    print("số pixel được chọn:", mask.sum())        # mong đợi: ~900 (ô 30x30)
```

## 8. Cách làm dần (đừng làm hết một lúc)
1. Thay code tạm bằng **Global Threshold lặp** → chạy test ở mục 7 → ra `[0 1]`,
   tách đúng ô vuông → commit.
2. Thêm `otsu` → test → commit.
3. Thêm `adaptive` → test → commit.
4. Thêm `morphology` → test → commit.
5. Thêm `chon_vung_tuy` (connected component) → test → commit.

## 9. Coi là XONG khi
- Cho ảnh giả (ô vuông sáng) → `segment` tách đúng ô đó (Dice với ô vuông > 0.95).
- Đầu ra là mask `{0,1}`, đúng kích thước.
- Cả 3 phương pháp `global` / `otsu` / `adaptive` đều chạy.
- Chọn đúng vùng tụy (không lấy nhầm vùng lớn nhất).

## 10. Phần báo cáo bạn phải viết
- Chương 2: Cơ sở lý thuyết + **Related Works (mục 2.2)** — tìm ≥3 bài báo trong
  5–10 năm gần đây, **dùng cùng dataset NIH Pancreas-CT**, lập bảng so sánh Dice.
- Mục 3.5–3.7 (phân ngưỡng, morphology, connected component).
- Mỗi mục 3.x trình bày đủ: **Đầu vào → Đầu ra → Mô tả bằng lời → Mã giả → Cách
  hiện thực → Kết quả**.

## 11. Câu hỏi Q&A bạn phải trả lời được (phần của B)
- Phân ngưỡng là gì? Công thức g(x,y) hoạt động thế nào?
- Otsu giả định gì về histogram (bimodal)? Ảnh CT có thỏa không?
- Vì sao KHÔNG chọn connected component lớn nhất cho tụy?
- Opening và Closing khác nhau thế nào?
- So sánh Global / Otsu / Adaptive: cái nào tốt hơn trên ảnh nhóm, vì sao?

## 12. Quy trình làm việc với GitHub (tóm tắt)
```bash
git clone <link-repo>          # tải repo về
cd pancreas-segmentation
pip install -r requirements.txt
git checkout -b b             # tạo nhánh riêng của mình
# ... code trong segment.py, chạy thử ...
git add segment.py
git commit -m "mô tả việc vừa làm"
git push origin b            # đẩy lên nhánh của mình (KHÔNG đẩy thẳng vào main)
```
Sau đó lên GitHub tạo Pull Request để trưởng nhóm xem và gộp.
