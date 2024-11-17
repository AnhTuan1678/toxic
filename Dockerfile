# Sử dụng image TensorFlow chính thức
FROM tensorflow/tensorflow:latest

# Tạo thư mục làm việc trong container
WORKDIR /app

# Copy file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn vào container
COPY . /app

# Mở cổng nếu cần
EXPOSE 3000

# Lệnh chạy ứng dụng (ví dụ: app.py)
CMD ["python", "app.py"]
