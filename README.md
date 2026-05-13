# Dự đoán điểm cuối kỳ (Score Prediction App)

Đây là một ứng dụng web đơn giản được viết bằng Flask, cho phép huấn luyện mô hình Hồi quy tuyến tính (Linear Regression) để dự đoán điểm cuối kỳ dựa vào điểm giữa kỳ.

## Cài đặt thư viện

Để chạy ứng dụng, bạn cần cài đặt các thư viện Python sau:

```bash
pip install flask pandas numpy scikit-learn openpyxl
```

## Cách chạy ứng dụng

1. Mở terminal/command prompt và di chuyển đến thư mục chứa ứng dụng:

2. Chạy file `app.py`:
   ```bash
   python app.py
   ```

3. Mở trình duyệt web và truy cập vào địa chỉ:
   [http://localhost:5000](http://localhost:5000)

## Hướng dẫn sử dụng

1. **Chuẩn bị dữ liệu**: Cần một file Excel (`.xlsx`) chứa dữ liệu điểm. Trong file bắt buộc phải chứa 2 cột mang tên:
   - `midterm`: Điểm giữa kỳ
   - `final`: Điểm cuối kỳ

2. **Huấn luyện mô hình**:
   - Tại giao diện web, nhấn vào **"Choose File"** để chọn file Excel.
   - Nhấn nút **"Tải lên & Huấn luyện"**.
   - Giao diện sẽ hiển thị thông báo "Huấn luyện thành công" kèm theo các thông số tổng quan của mô hình (độ chính xác, số mẫu, sai số Mean Squared Error).

3. **Dự đoán**:
   - Sau khi file và mô hình đã được xử lý xong, ô nhập điểm sẽ xuất hiện.
   - Nhập điểm giữa kỳ (từ 0 đến 10).
   - Nhấn nút **"Dự đoán"** để xem kết quả dự đoán điểm cuối kỳ dựa theo mô hình.