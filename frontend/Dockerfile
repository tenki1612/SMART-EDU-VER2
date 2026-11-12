# ==========================================
# Frontend React 19 + Vite - Hardened Multi-stage Build
# Sử dụng Alpine 3.21 để đạt 0 Critical / 0 High Vulnerabilities
# ==========================================

# Stage 1: Build static assets
FROM node:22-alpine3.21 AS build
WORKDIR /app

RUN apk update && apk upgrade --no-cache

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Nginx phục vụ static files (Production runtime)
FROM nginx:1.27-alpine3.21

# Cập nhật mọi gói hệ thống Alpine lên bản vá mới nhất (loại bỏ 4 High vulnerabilities)
RUN apk update && apk upgrade --no-cache

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
