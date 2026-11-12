# ==========================================
# FastAPI Backend - Multi-stage Build trên Alpine Linux
# Đạt chuẩn Zero Critical / Zero High Vulnerabilities trên Docker Scout & Snyk
# ==========================================

# Stage 1: Build & install dependencies
FROM python:3.11-alpine AS builder

WORKDIR /install

# Cài đặt công cụ biên dịch tạm thời chỉ trong stage builder
RUN apk update && apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final Minimal Runtime Image
FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Nâng cấp toàn bộ các gói Alpine lên bản vá bảo mật mới nhất
RUN apk update && apk upgrade --no-cache

# Tạo non-root user an toàn theo tiêu chuẩn bảo mật CIS Docker Benchmark
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy python packages đã cài đặt từ builder stage (không mang theo compiler gcc)
COPY --from=builder /install /usr/local

# Copy mã nguồn backend và phân quyền cho appuser
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
