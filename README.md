# Hướng dẫn: Giả lập và Huấn luyện Mô hình

Dự án này hướng dẫn cách thiết lập một hệ thống bao gồm:
- **Server nhận dữ liệu**
- **Server gửi dữ liệu**
- **Huấn luyện mô hình học máy/Deep Learning** với Spark.

## Cách thực hiện

Thực hiện lần lượt các bước sau trên terminal (sử dụng Visual Studio Code hoặc terminal bất kỳ):

1.  **Khởi chạy server nhận dữ liệu:**
    ```bash
    python receiver.py
    ```

2.  **Khởi chạy server gửi dữ liệu:**
    ```bash
    python sender.py
    ```

3.  **Tiến hành huấn luyện mô hình với Spark:**
    ```bash
    spark-submit train_model.py
    ```
