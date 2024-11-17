# Sử dụng image Python chính thức
FROM python:3.12.6

# Tạo thư mục làm việc trong container
WORKDIR /app

# Copy file requirements.txt vào container
COPY requirements.txt .

# Tạo môi trường ảo và cài đặt các thư viện từ requirements.txt
RUN python -m venv .venv && \
    ./.venv/bin/pip install -r requirements.txt

# Copy mã nguồn vào container
COPY . /app

# Thiết lập môi trường ảo khi chạy container
ENV PATH="/.venv/bin:$PATH"

# Mở cổng nếu cần
EXPOSE 3000

# Lệnh chạy ứng dụng (ví dụ: app.py hoặc app.js)
CMD ["python", "app.py"]
