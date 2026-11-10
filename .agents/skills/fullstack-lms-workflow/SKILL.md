---
name: fullstack-lms-workflow
description: Quy trình chuẩn xây dựng hệ thống quản lý đào tạo / trung tâm ngoại ngữ (LMS/CRM) full-stack với FastAPI, SQLAlchemy, Pydantic v2, React 19, JavaScript (JSX), Vite và Tailwind CSS theo mô hình Modular Monolith DDD-Lite và Sơ đồ lớp OOAD.
---

# Fullstack Educational LMS Development Workflow

Quy trình chuẩn hóa để thiết kế, triển khai, kiểm thử và tối ưu hóa hệ thống Quản lý Đào tạo / Trung tâm Ngoại ngữ (SMART-EDU LMS) theo thiết kế hướng đối tượng (OOAD), kiến trúc phân lớp chuẩn và sơ đồ lớp chi tiết.

---

## 1. NGUYÊN TẮC THIẾT KẾ & SƠ ĐỒ LỚP HƯỚNG ĐỐI TƯỢNG (OOAD CLASS DIAGRAM)

### 1.1. Phân cấp Kế thừa Lớp Người dùng (User Hierarchy):
- **`NguoiDung` (Lớp cơ sở / Base Class):**
  - Thuộc tính: `maNguoiDung` (ID), `tenDangNhap`, `matKhau` (Hashed Bcrypt), `email`, `soDienThoai`, `trangThai` (`is_active`, `is_locked`), `ngayTao`.
  - Phương thức: `dangNhap()`, `dangXuat()`, `doiMatKhau()`, `quenMatKhau()`.
- **`QuanTriVien` (Kế thừa `NguoiDung`):**
  - Phương thức: `quanLyTaiKhoan()`, `quanLyKhoaHoc()`, `quanLyLopHoc()`, `quanLyPhongHoc()`, `dangKyTaiKhoanPhuHuynh()`.
- **`NhanVienHocVu` (Kế thừa `NguoiDung`):**
  - Phương thức: `duyetDangKy()`, `tuChoiDangKy()`, `taoThoiKhoaBieu()`, `xacNhanKetQua()`, `dangKyTaiKhoanPhuHuynh()`.
- **`GiaoVien` (Kế thừa `NguoiDung`):**
  - Thuộc tính: `chuyenMon`, `maGiaoVien`, `bangCap`.
  - Phương thức: `nhapDiem()`, `capNhatDiem()`, `xemLichDay()`, `dangKyTaiKhoanPhuHuynh()`.
- **`HocVien` (Kế thừa `NguoiDung`):**
  - Thuộc tính: `maHocVien`, `ngaySinh`, `gioiTinh`, `diaChi`.
  - Phương thức: `dangKyLop()`, `huyYeuCauDangKy()`, `xemDiem()`, `xemLichHoc()`.
- **`PhuHuynh` (Kế thừa `NguoiDung`):**
  - Thuộc tính: `maPhuHuynh`.
  - Phương thức: `xemThongTinHocVien()`, `xemTrangThaiDangKy()`, `xemDiem()`, `xemLichHoc()`.

> **Quy tắc Nghiệp vụ Đặc biệt (Self Parent Account Registration):**
> Các tài khoản nội bộ trung tâm gồm **`ADMIN` (Quản trị viên)**, **`ACADEMIC_STAFF` (Học vụ)** và **`TEACHER` (Giáo viên)** được quyền tự đăng ký thêm **1 tài khoản Phụ huynh (`PARENT`)** cho bản thân mình để giám hộ con em học tập tại trung tâm. Khi đăng ký, hệ thống giữ nguyên thông tin cá nhân (Họ tên, email định danh cá nhân) và số điện thoại liên lạc (`soDienThoai`), đồng thời tạo liên kết giám hộ cha-con/mẹ-con an toàn.

---

### 1.2. Các Lớp Thực thể Quản lý Đào tạo & Điểm số:
1. **`KhoaHoc`:**
   - Thuộc tính: `maKhoaHoc`, `tenKhoaHoc`, `capDoMucTieu`, `moTa`, `trangThai`.
   - Phương thức: `themKhoaHoc()`, `capNhatKhoaHoc()`.
2. **`LopHoc`:**
   - Thuộc tính: `maLop`, `tenLop`, `siSoToiDa`, `siSoHienTai`, `trangThai`, `ngayBatDau`, `ngayKetThuc`, `maKhoaHoc`.
   - Phương thức: `themHocVien()`, `capNhatTrangThai()`.
3. **`ThoiKhoaBieu` & `BuoiHoc`:**
   - `ThoiKhoaBieu`: `maTKB`, `trangThai`, `maLop` | Phương thức: `taoBuoiHoc()`, `capNhatBuoiHoc()`, `kiemTraXungDot()`, `xacNhan()`.
   - `BuoiHoc`: `maBuoi`, `ngayHoc`, `gioBatDau`, `gioKetThuc`, `trangThai`, `maTKB`, `maGiaoVien`, `maPhong`.
4. **`PhongHoc`:**
   - Thuộc tính: `maPhong`, `tenPhong`, `sucChua`, `trangThai`.
5. **`YeuCauDangKy`:**
   - Thuộc tính: `maYeuCau`, `ngayDangKy`, `trangThai`, `lyDoTuChoi`, `maHocVien`, `maLop`.
   - Phương thức: `guiYeuCau()`, `huyYeuCau()`.
6. **`Diem` & `KetQuaHocTap`:**
   - `Diem`: `maDiem`, `loaiDiem`, `diemSo`, `ngayNhap`, `maHocVien`, `maLop` | Phương thức: `kiemTraHopLe()`.
   - `KetQuaHocTap`: `maKetQua`, `diemTrungBinh`, `xepLoai`, `trangThaiXacNhan`, `maHocVien`, `maLop` | Phương thức: `tongHopKetQua()`, `xacNhanKetQua()`.

---

## 2. NGUYÊN TẮC THIẾT KẾ CỐT LÕI (ARCHITECTURE PRINCIPLES)

1. **Modular Monolith (DDD-Lite):**
   - Đóng gói theo nghiệp vụ (Feature-first / Bounded Context), không chia phẳng (Flat Layered).
   - Mỗi module nghiệp vụ sở hữu đầy đủ 4 tầng riêng biệt:
     $$\text{Router (HTTP)} \longrightarrow \text{Schema (DTO)} \longrightarrow \text{Service (Logic)} \longrightarrow \text{Repository/Model (DB)}$$
2. **Zero-Config Database Defaults:**
   - Cấu hình mặc định sử dụng SQLite cục bộ (`database/language_center.db`) để chạy ngay không cần cài đặt.
   - Hỗ trợ chuyển đổi sang PostgreSQL 16 thông qua Docker Compose và `.env`.
3. **Phân Quyền Vai Trò (RBAC) 5 Cấp & Phân Quyền Kép:**
   - 5 vai trò phân lập: `ADMIN`, `ACADEMIC_STAFF`, `TEACHER`, `STUDENT`, `PARENT`.
   - Bảo vệ an toàn từng endpoint bằng FastAPI Dependency Injection (`require_roles([...])`).
4. **Bảo Mật Nghiêm Ngặt & Phòng Vệ Đa Tầng:**
   - Mã hóa mật khẩu 1 chiều bằng thuật toán `bcrypt` (Salt rounds = 12).
   - Phòng chống brute-force: Tự động khóa tài khoản tạm thời 15 phút sau 5 lần nhập sai liên tiếp.
   - Khôi phục mật khẩu an toàn bằng mã OTP 6 chữ số ngẫu nhiên thời hạn 15 phút.
5. **Trải Nghiệm Giao Diện Người Dùng (Operate Mode):**
   - Sử dụng phông `JetBrains Mono` kết hợp `tabular-nums` cho số liệu.
   - Trải nghiệm phi chặn (Zero native alerts): Thay thế 100% bằng Toast nổi và Modal xác nhận.

---

## 3. QUY TRÌNH TRIỂN KHAI THEO 11 BOUNDED CONTEXTS

1. `auth`: Xác thực JWT, đăng nhập, đăng xuất, tự đăng ký học viên, đăng ký thêm tài khoản phụ huynh cho Admin/Staff/Teacher giữ nguyên số điện thoại, khôi phục mật khẩu OTP.
2. `accounts`: Quản lý tài khoản, nâng quyền vai trò, khóa/mở khóa tức thì, cấp lại mật khẩu.
3. `courses`: Quản lý chương trình đào tạo, chuẩn đầu ra mục tiêu (IELTS, TOEIC), học phí (`KhoaHoc`).
4. `students`: Hồ sơ học viên (`HocVien`), mã định danh, lịch sử học tập.
5. `teachers`: Hồ sơ giảng viên (`GiaoVien`), mã định danh, chuyên môn, lịch giảng dạy.
6. `classes`: Lớp học (`LopHoc`), sức chứa tối đa, sĩ số hiện tại, gán giáo viên.
7. `classrooms`: Phòng học (`PhongHoc`), sức chứa, tình trạng thiết bị.
8. `enrollments`: Quy trình đăng ký lớp (`YeuCauDangKy`), học vụ xét duyệt hoặc từ chối.
9. `schedules`: Thời khóa biểu (`ThoiKhoaBieu`, `BuoiHoc`), thuật toán chống xung đột phòng học & giáo viên thời gian thực.
10. `grades`: Điểm thành phần (`Diem`), tính điểm trung bình tổng kết trọng số và khóa kết quả (`KetQuaHocTap`).
11. `progression_parent`: Ràng buộc tiên quyết nâng khóa, cổng phụ huynh (`PhuHuynh`) tra cứu kết quả con em.
