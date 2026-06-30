"""
RÁP CẢ PIPELINE: A -> B -> C (trưởng nhóm giữ file này)

Chạy:  python main.py
Mục đích: SMOKE TEST — chạy nhanh A->B->C để chắc 3 phần đang khớp nhau.
(Phân tích đầy đủ / so sánh phương pháp là việc của experiments.py, không phải file này.)

Ưu tiên chạy trên ẢNH CT THẬT trong data/. Nếu chưa có data thì tự lùi về
ảnh giả (ô vuông sáng) để vẫn chạy được, không bao giờ lỗi.
"""
import glob
import numpy as np
from preprocess import preprocess
from segment import segment
from evaluate import dice, iou, precision, recall


def tao_anh_gia():
    """Dự phòng khi chưa có dữ liệu thật: nền tối + 1 ô vuông sáng = vùng cần tách."""
    img = np.zeros((100, 100), dtype=np.uint8)
    img[35:65, 35:65] = 200
    gt = np.zeros((100, 100), dtype=np.uint8)
    gt[35:65, 35:65] = 1
    return img, gt


def chay_mot_lat(img, gt, method="otsu"):
    """Chạy trọn A->B->C cho 1 lát, trả về 4 chỉ số."""
    img_xl = preprocess(img)              # A: tiền xử lý
    mask = segment(img_xl, method)        # B: phân ngưỡng
    return (dice(mask, gt), iou(mask, gt),     # C: đánh giá
            precision(mask, gt), recall(mask, gt))


if __name__ == "__main__":
    method = "otsu"
    so_lat = len(glob.glob("data/img_*.npy"))

    if so_lat > 0:
        # --- Có ảnh CT thật ---
        from data_loader import load_image
        D = I = P = R = 0.0
        for i in range(so_lat):
            img, gt = load_image(i)
            d, j, p, r = chay_mot_lat(img, gt, method)
            D += d; I += j; P += p; R += r
        n = so_lat
        print(f"Pipeline chạy OK trên {n} lát CT thật | phương pháp = {method}")
        print(f"Trung bình -> Dice={D/n:.3f} | IoU={I/n:.3f} | "
              f"Precision={P/n:.3f} | Recall={R/n:.3f}")
        print("(Dice thấp là dự kiến: tụy cùng độ xám với mô mềm lân cận nên "
              "ngưỡng tô lan ra ngoài.)")
    else:
        # --- Chưa có data -> ảnh giả ---
        img, gt = tao_anh_gia()
        d, j, p, r = chay_mot_lat(img, gt, method)
        print("Chưa thấy data/ -> chạy ảnh giả để kiểm tra pipeline.")
        print(f"Dice={d:.3f} | IoU={j:.3f} | Precision={p:.3f} | Recall={r:.3f}")

    print("Pipeline 3 phần (A->B->C) khớp nhau, không lỗi.")
