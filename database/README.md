# 🗄️ CƠ SỞ DỮ LIỆU HỆ THỐNG SMART-EDU LMS

Thư mục này chứa toàn bộ cấu trúc và dữ liệu mẫu của Cơ sở dữ liệu Hệ thống Quản lý Trung tâm Ngoại ngữ (SMART-EDU LMS) được tách độc lập phục vụ phát triển, kiểm thử hoặc tích hợp backend mới.

---

## 📁 1. CÁC TỆP TRONG THƯ MỤC DATABASE

| Tệp | Định dạng | Mục đích |
|---|---|---|
| `language_center.db` | SQLite Database Binary | Cơ sở dữ liệu SQLite hoàn chỉnh có sẵn 12 bảng và dữ liệu mẫu. Dùng trực tiếp không cần cài đặt máy chủ SQL. |
| `language_center_dump.sql` | SQL DDL & DML (SQLite) | Bản dump toàn bộ câu lệnh `CREATE TABLE` và `INSERT INTO` theo chuẩn cú pháp SQLite. |
| `init_postgres.sql` | SQL DDL & DML (PostgreSQL) | Bản script khởi tạo tương thích hoàn toàn với PostgreSQL 16+, tự động nạp dữ liệu và cấu hình sequences. |

---

## 📊 2. DANH SÁCH 12 BẢNG DỮ LIỆU (12 TABLES)

Hệ thống được thiết kế theo chuẩn quan hệ 3NF đảm bảo toàn vẹn dữ liệu:

1. **`users`**: Tài khoản người dùng, phân quyền 5 vai trò (`ADMIN`, `ACADEMIC_STAFF`, `TEACHER`, `STUDENT`, `PARENT`), mã hóa mật khẩu bcrypt, khóa tài khoản tạm thời khi nhập sai.
2. **`courses`**: Danh mục chương trình đào tạo & khóa học ngoại ngữ (IELTS 6.5, IELTS 7.5+, TOEIC 750), học phí, chuẩn đầu ra.
3. **`classrooms`**: Danh mục phòng học (Lý thuyết, Lab, Hội trường), sức chứa chỗ ngồi và trạng thái khả dụng.
4. **`teachers`**: Hồ sơ giảng viên (liên kết 1-1 với `users`), mã giáo viên (`GVxxxx`), học vị và chuyên môn.
5. **`students`**: Hồ sơ học viên (liên kết 1-1 với `users`), mã số học viên (`YY-XXXXX`), ngày sinh, tình trạng học phí.
6. **`classes`**: Danh sách lớp học mở theo khóa học, giảng viên phụ trách, sĩ số tối đa & sĩ số hiện tại, ngày khai giảng.
7. **`class_students`**: Danh sách học viên tham gia từng lớp học.
8. **`enrollment_requests`**: Quy trình nộp đơn đăng ký lớp học và xét duyệt ghi danh của nhân viên học vụ.
9. **`schedule_sessions`**: Lịch học chi tiết từng buổi học (ngày học, ca học, phòng học, giảng viên, lớp học).
10. **`grade_records`**: Sổ chấm điểm trọng số (20% Chuyên cần, 30% Giữa kỳ, 50% Cuối kỳ), xếp loại Đạt/Chưa đạt và cờ khóa sổ điểm (`is_confirmed`).
11. **`course_progressions`**: Theo dõi điều kiện tiên quyết và lộ trình chuyển khóa học của học viên.
12. **`parent_students`**: Liên kết giám hộ giữa tài khoản Phụ huynh và Học viên (con em).

---

## 🔑 3. TÀI KHOẢN MẪU KHỞI TẠO (5 VAI TRÒ)

Mật khẩu mặc định đã được băm an toàn theo chuẩn `bcrypt`:

| Vai trò (Role) | Username | Password | Tên người dùng |
|---|---|---|---|
| **Admin** | `admin` | `admin123` | Nguyễn Văn Quản Trị |
| **Nhân viên học vụ (Staff)** | `staff` | `staff123` | Trần Thị Học Vụ |
| **Giáo viên (Teacher)** | `teacher` | `teacher123` | ThS. Lê Hoàng Nam |
| **Học viên (Student)** | `student` | `student123` | Phạm Minh Khang |
| **Phụ huynh (Parent)** | `parent` | `parent123` | Phạm Quốc Hùng |

---

## 🚀 4. HƯỚNG DẪN SỬ DỤNG DATABASE

### Cách 1: Sử dụng SQLite (Zero-config, chạy ngay)
- Mở trực tiếp file `database/language_center.db` bằng các công cụ quản trị giao diện như:
  - **DBeaver** / **TablePlus** / **DB Browser for SQLite**
  - Tiện ích mở rộng **SQLite Viewer** trên VS Code
- Hoặc quản trị qua **Prisma Studio**:
  ```bash
  npm run prisma:sqlite:studio
  ```
  Truy cập: `http://localhost:5555`

### Cách 2: Khởi động PostgreSQL 16 bằng Docker
Docker Compose đã được cấu hình tự động ánh xạ `init_postgres.sql` vào thư mục khởi tạo ban đầu:
```bash
docker compose up -d
```
- Host: `localhost`
- Port: `5432`
- Database: `language_center`
- Username: `postgres`
- Password: `postgrespassword2026`

Toàn bộ 12 bảng và dữ liệu mẫu sẽ được nạp sẵn sàng ngay khi container khởi động.
