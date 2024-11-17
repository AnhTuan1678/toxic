# Sử dụng Python 3.12 làm base image
FROM python:3.10

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép tất cả các tệp trong thư mục hiện tại vào container
COPY . /app

# Cài đặt các thư viện phụ thuộc từ file requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mở cổng ứng dụng (nếu cần, ví dụ với Flask hoặc FastAPI)
EXPOSE 5000

# Lệnh để chạy ứng dụng (thay "app.py" bằng tên tệp chính của bạn)
CMD ["python", "app.py"]
