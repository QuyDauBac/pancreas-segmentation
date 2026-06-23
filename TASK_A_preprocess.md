# NHIỆM VỤ THÀNH VIÊN A — TIỀN XỬ LÝ ẢNH (`preprocess.py`)

> **Nếu bạn đưa file này cho một trợ lý AI:** đây là toàn bộ phần việc của thành
> viên A trong đồ án. Hãy nhờ AI giải thích từng khái niệm, hướng dẫn viết code
> từng bước theo các mục bên dưới, và kiểm tra giúp kết quả. Mọi thông tin cần
> thiết đều nằm trong file này.

---

## 1. Bối cảnh đồ án (đọc để hiểu mình đang làm gì)

Đồ án: **Phân đoạn ảnh tuyến tụy trên ảnh CT** bằng kỹ thuật xử lý ảnh truyền
thống (KHÔNG dùng Deep Learning). "Phân đoạn" nghĩa là tô ra đúng vùng tuyến tụy
trong ảnh chụp cắt lớp (CT).

Cả nhóm chia pipeline thành chuỗi 4 bước, dữ liệu chạy qua từng người:

```
D (load ảnh + HU windowing) -> A (TIỀN XỬ LÝ) -> B (phân ngưỡng) -> C (đánh giá Dice)
```

**Bạn là A — bước tiền xử lý.** Nhiệm vụ: làm ảnh sạch nhiễu hơn và rõ tương phản
hơn, để bước sau (B) tách tụy dễ hơn. Bạn KHÔNG cần biết B hay C làm gì bên trong
— chỉ cần nhận đúng đầu vào và trả đúng đầu ra theo quy ước.

> 💡 **Lưu ý quan trọng:** việc chuyển ảnh CT thô (đơn vị HU) thành ảnh xám là của
> **D** (HU windowing nằm trong `data_loader.py`). Bạn **nhận sẵn ảnh xám rồi**,
> nên KHÔNG phải làm HU windowing. Phần của bạn là xử lý miền không gian thuần —
> đúng tên đề tài và dễ trình bày nhất.

## 2. Quy ước bắt buộc (sai là cả nhóm ráp code bị lỗi)

- Bạn viết hàm tên `preprocess(img)` trong file `preprocess.py`.
- **Đầu vào:** ảnh xám `uint8` 0–255 (do D đưa, đã HU windowing).
- **Đầu ra:** ảnh xám, kiểu `uint8`, giá trị từ `0` đến `255`.

Giải thích cho người mới: "ảnh xám" là ảnh chỉ có một kênh độ sáng (không màu).
"uint8" là kiểu số nguyên 0–255. Mọi ảnh bạn trả ra phải đúng dạng này.

## 3. File `preprocess.py` đã có sẵn code tạm — bạn làm gì với nó?

Trong file đã có sẵn một hàm `preprocess` **làm tạm** (chỉ đảm bảo đúng định dạng)
kèm dòng ghi chú `# TODO (A)`. Code tạm đó chỉ để pipeline chạy thử được. **Việc
của bạn: giữ nguyên tên hàm và quy ước đầu ra, thay phần ruột bên trong bằng các
bước xử lý thật.** Đừng đổi tên hàm `preprocess`.

## 4. Các bước phải làm (theo ĐÚNG thứ tự)

### Bước 1 — Khử nhiễu (CHỈ CHỌN MỘT bộ lọc)
Nhiễu là các đốm lốm đốm làm ảnh xấu. Hai loại lọc:
- **Median filter (lọc trung vị):** với mỗi điểm ảnh, lấy 9 điểm trong ô 3×3 quanh
  nó, sắp xếp, lấy giá trị giữa. Hợp với nhiễu "muối tiêu" (đốm trắng/đen).
- **Gaussian filter:** làm mờ nhẹ theo trọng số. Hợp với nhiễu Gaussian.

⚠️ **Chỉ dùng MỘT trong hai, không xếp cả hai liên tiếp** — vì làm trơn 2 lần sẽ
mờ mất biên tụy (tụy nhỏ, mất biên là tách sai). Để chọn lọc nào qua tham số
`denoise` ("median" / "gaussian") cũng được, nhưng mỗi lần chỉ chạy một.

### Bước 2 — Histogram Equalization (cân bằng sáng)
Kỹ thuật kéo dãn độ tương phản: dồn các mức xám cho trải đều ra, ảnh rõ hơn. Cách
làm: đếm số điểm ở mỗi mức xám → tính phân bố tích lũy → ánh xạ lại mức xám mới
theo công thức tích lũy (công thức có trong slide môn học).

⚠️ **Đặt bước này SAU khử nhiễu, không phải trước** — vì cân bằng sáng làm rõ cả
nhiễu, nếu chưa khử nhiễu mà cân bằng trước thì nhiễu bị khuếch đại.

### Bước 3 — Crop giữa ảnh (tùy chọn, làm cho đơn giản)
Tụy nằm gần giữa vùng bụng. Nếu muốn, cắt lấy phần giữa ảnh (ví dụ vùng trung tâm
60%) để bớt phần thừa hai bên. **Chỉ cắt cố định ở giữa cho đơn giản** — đừng làm
ROI "thông minh" tự dò, vừa phức tạp vừa khó trả lời vấn đáp. Bước này có thể bỏ.

## 5. Gợi ý code

- Thầy yêu cầu báo cáo có **mã giả + phần tự hiện thực**, nên hãy **TỰ VIẾT** hàm
  Median filter và Histogram Equalization theo công thức trong slide (vòng lặp
  duyệt từng điểm ảnh). Đây là phần ghi điểm.
- Có thể dùng thư viện `cv2` (`cv2.medianBlur`, `cv2.equalizeHist`) để **so sánh,
  kiểm chứng** kết quả bản tự viết — nhưng bản nộp nên có bản tự cài.

Khung hàm sẽ phình ra đại khái như sau (bạn viết thêm các hàm con trong cùng file):

```python
import numpy as np

def preprocess(img, denoise="median"):
    img = ve_xam_neu_can(img)             # phòng hờ ảnh màu -> xám
    img = khu_nhieu(img, denoise)         # bước 1 (median HOẶC gaussian)
    img = histogram_equalization(img)     # bước 2
    img = crop_giua(img)                  # bước 3 (tùy chọn)
    return img.astype(np.uint8)           # luôn trả uint8 0..255

# TODO (A): viết các hàm con ở dưới
def khu_nhieu(img, denoise): ...
def histogram_equalization(img): ...
```

## 6. Cách tự kiểm tra phần mình (không cần chờ ai)

Thêm đoạn này vào cuối `preprocess.py` rồi chạy `python preprocess.py`:

```python
if __name__ == "__main__":
    import numpy as np
    # ảnh giả: dải xám + vài đốm nhiễu trắng
    img = np.tile(np.arange(0, 256, 2, dtype=np.uint8), (128, 1))
    out = preprocess(img)
    print("kiểu:", out.dtype, "| min:", out.min(), "| max:", out.max())
    # mong đợi: kiểu uint8, min>=0, max<=255
```

## 7. Coi là XONG khi
- `preprocess(ảnh)` trả ra ảnh xám `uint8`, giá trị trong 0–255.
- Lấy 1 ảnh sạch → thêm nhiễu → lọc → ảnh nhìn đỡ nhiễu, rõ tương phản hơn.
- (Nếu dùng PSNR để kiểm tra khử nhiễu) PSNR sau lọc cao hơn ảnh nhiễu.

## 8. Phần báo cáo bạn phải viết
- Chương 1 (Giới thiệu) + mục 3.2–3.3 (khử nhiễu, Histogram Equalization).
- Mỗi mục 3.x trình bày đủ: **Đầu vào → Đầu ra → Mô tả bằng lời → Mã giả → Cách
  hiện thực → Kết quả (ảnh trước/sau)**.

> (HU windowing là phần của D — D viết ở mục 4.1 Tập dữ liệu, bạn không phải viết.)

## 9. Câu hỏi Q&A bạn phải trả lời được (phần của A)
- Histogram Equalization để làm gì, làm thế nào?
- Median và Gaussian filter khác nhau ra sao, khi nào dùng cái nào?
- Vì sao đặt Histogram Equalization SAU khử nhiễu chứ không phải trước?
- Vì sao không xếp cả median + gaussian liên tiếp?

## 10. Quy trình làm việc với GitHub (tóm tắt)
```bash
git clone <link-repo>          # tải repo về
cd pancreas-segmentation
pip install -r requirements.txt
git checkout -b a              # tạo nhánh riêng của mình
# ... code trong preprocess.py, chạy thử ...
git add preprocess.py
git commit -m "mô tả việc vừa làm"
git push origin a             # đẩy lên nhánh của mình (KHÔNG đẩy thẳng vào main)
```
Sau đó lên GitHub tạo Pull Request để trưởng nhóm xem và gộp.
