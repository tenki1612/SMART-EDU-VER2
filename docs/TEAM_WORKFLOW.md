# KẾ HOẠCH PHÂN CHIA CÔNG VIỆC & HƯỚNG DẪN PHÁT TRIỂN DỰ ÁN SMART-EDU LMS (VER2)

> **Dự án:** Hệ thống Quản lý Trung tâm Ngoại ngữ (SMART-EDU LMS)  
> **Repository:** https://github.com/tenki1612/SMART-EDU-VER2.git  
> **Kiến trúc:** Decoupled Architecture (Frontend React 19 SPA + Backend Modular Monolith DDD-Lite + Database PostgreSQL/SQLite)  
> **Mục tiêu:** Nhóm 3 thành viên thực hiện hoàn thiện 11 Bounded Contexts tương ứng 11 GitHub Issues.

---

## 1. PHÂN CHIA NHIỆM VỤ CHI TIẾT (TEAM ASSIGNMENT)

### 👤 DANH (Phụ trách Issues #1, #2, #3) - Phân hệ Hạt nhân & Đào tạo
- **Issue #1: Xác thực người dùng & Quản lý phiên (Authentication - Auth Context)**
  - Chức năng: Đăng nhập hệ thống bằng mật khẩu băm Bcrypt, cấp phát và giải mã JWT Bearer Token (thời hạn 24h), quản lý thông tin tài khoản cá nhân (`/api/v1/auth/me`).
  - Phân quyền: Cấu hình Dependency Injection kiểm soát vai trò (`require_roles`).
- **Issue #2: Quản trị Tài khoản người dùng (Accounts Context)**
  - Chức năng: CRUD tài khoản cho 5 nhóm vai trò (`ADMIN`, `STAFF`, `TEACHER`, `STUDENT`, `PARENT`), cơ chế đổi mật khẩu, cơ chế tự động khóa tài khoản tạm thời 15 phút nếu nhập sai quá 5 lần.
- **Issue #3: Quản lý Khóa học & Biểu phí (Courses Context)**
  - Chức năng: Quản lý danh mục khóa đào tạo (IELTS, TOEIC, Giao tiếp), thời lượng học (số tuần), mức học phí chuẩn, chuẩn đầu ra (Target Level) và điều kiện tiên quyết (Prerequisite Course).

---

### 👤 DUY (Phụ trách Issues #4, #5, #6, #7) - Phân hệ Con người & Cơ sở vật chất
- **Issue #4: Quản lý Hồ sơ Học viên (Students Context)**
  - Chức năng: Hồ sơ lý lịch học viên, theo dõi lịch sử tham gia các lớp học, tình trạng học phí, liên kết mã học viên với tài khoản phụ huynh quản lý.
- **Issue #5: Quản lý Hồ sơ Giảng viên (Teachers Context)**
  - Chức năng: Quản lý đội ngũ giảng viên, thông tin bằng cấp/chứng chỉ, phân công môn dạy chuyên trách, tra cứu lịch giảng dạy cá nhân.
- **Issue #6: Điều phối & Quản lý Lớp học (Classes Context)**
  - Chức năng: Mở lớp học mới, cấu hình ngày khai giảng - bế giảng, phân công giáo viên phụ trách, kiểm soát sĩ số tối đa (`capacity`), cảnh báo khi lớp vượt quá sĩ số hoặc không đủ điều kiện mở lớp.
- **Issue #7: Quản lý Phòng học & Thiết bị (Classrooms Context)**
  - Chức năng: Quản lý danh mục phòng học, sức chứa tối đa theo phòng, tình trạng trang thiết bị (máy chiếu, âm thanh, điều hòa) và cờ trạng thái sẵn sàng sử dụng.

---

### 👤 TOÀN (Phụ trách Issues #8, #9, #10, #11) - Phân hệ Xếp lịch, Sổ điểm & Tốt nghiệp
- **Issue #8: Quản lý Đăng ký & Tuyển sinh (Enrollments Context)**
  - Chức năng: Tiếp nhận đơn đăng ký lớp trực tuyến, luồng phê duyệt học viên vào lớp của Học vụ (`CONFIRMED`), từ chối đơn kèm lý do (`REJECTED`), tự động cập nhật sĩ số lớp học.
- **Issue #9: Quản lý Thời khóa biểu & Thuật toán Xung đột (Schedules Context)**
  - Chức năng: Lập lịch học từng buổi (`session_date`, giờ bắt đầu, giờ kết thúc).
  - Thuật toán cốt lõi: Phát hiện va chạm lịch thời gian thực theo công thức `(Start_A < End_B) AND (End_A > Start_B)` trên cả 2 tài nguyên: Phòng học (`classroom_id`) và Giáo viên (`teacher_id`).
- **Issue #10: Quản lý Sổ điểm & Thuật toán Trọng số (Grades Context)**
  - Chức năng: Bảng điểm theo lớp, tính điểm tổng kết: `0.2 * Attendance + 0.3 * Midterm + 0.5 * Final`. ĐẠT khi Tổng kết >= 5.0 và Cuối kỳ >= 4.0.
  - Cơ chế Khóa sổ điểm (`is_confirmed = True`): Khi học vụ đã duyệt khóa điểm, đóng băng toàn bộ quyền sửa điểm của giảng viên.
- **Issue #11: Cổng Phụ huynh & Xét Chuyển khóa (Progression & Parent Portal)**
  - Chức năng: Cổng tra cứu tiến trình học tập của phụ huynh; thẩm định điều kiện tiên quyết (đã đạt và đã khóa điểm ở khóa trước) trước khi duyệt lên khóa tiếp theo.

---

## 2. HƯỚNG DẪN CLONE CODE & THIẾT LẬP MÔI TRƯỜNG PHÁT TRIỂN

### Bước 1: Clone Repository về máy tính
Mở Terminal / PowerShell và chạy lệnh:
```bash
git clone https://github.com/tenki1612/SMART-EDU-VER2.git
cd SMART-EDU-VER2
```

### Bước 2: Khởi động Frontend (React 19 + Vite 8)
1. Cài đặt thư viện:
   ```bash
   cd frontend
   npm install
   ```
2. Khởi chạy máy chủ giao diện:
   ```bash
   npm run dev
   ```
   *(Hoặc trên Windows: nhấp đúp file `start_frontend.bat` ở thư mục gốc).*
3. Truy cập trình duyệt: `http://localhost:5173`.

### Bước 3: Thiết lập Cơ sở dữ liệu (Database)
Hệ thống hỗ trợ 2 tùy chọn CSDL đã chuẩn hóa 12 bảng trong thư mục `database/`:
- **Tùy chọn A - SQLite (Khuyên dùng khi lập trình nhanh):** Có sẵn file `database/language_center.db`, không cần cài đặt.
  - Xem dữ liệu bằng Prisma Studio:
    ```bash
    npm run prisma:sqlite:studio
    ```
    Truy cập: `http://localhost:5555`.
- **Tùy chọn B - PostgreSQL 16 qua Docker:**
  ```bash
  docker compose up -d
  ```
  Container sẽ tự nạp dữ liệu từ `database/init_postgres.sql`.

---

## 3. QUY TRÌNH THAO TÁC CÔNG VIỆC VỚI GIT & GITHUB

Để tránh xung đột code (conflict) giữa 3 người, toàn bộ nhóm phải tuân thủ nghiêm ngặt quy trình làm việc theo nhánh (Git Feature Branch Workflow):

### Quy tắc tạo nhánh (Branch Naming):
Mỗi thành viên làm Issue nào thì tạo nhánh riêng từ `main`:
- Cú pháp: `feat/issue-<số_issue>-<tên_ngắn>`
- Ví dụ:
  - Danh: `git checkout -b feat/issue-1-auth`
  - Duy: `git checkout -b feat/issue-4-students`
  - Toàn: `git checkout -b feat/issue-9-schedules`

### Chu trình làm việc hàng ngày:
1. **Trước khi bắt đầu code:** Luôn kéo code mới nhất từ `main` về:
   ```bash
   git checkout main
   git pull origin main
   git checkout <nhanh_cua_ban>
   git merge main
   ```
2. **Commit công việc rõ ràng:**
   ```bash
   git add .
   git commit -m "feat(auth): implement JWT login and password hashing"
   git push origin <nhanh_cua_ban>
   ```
3. **Tạo Pull Request (PR):**
   - Vào GitHub: `https://github.com/tenki1612/SMART-EDU-VER2/pulls`
   - Bấm **New Pull Request**, chọn nhánh của bạn merge vào `main`.
   - Ghi rõ nội dung và liên kết tới Issue (Ví dụ: `Closes #1`, `Closes #4`).
   - Yêu cầu ít nhất 1 thành viên khác review kiểm tra trước khi bấm **Merge**.

---

## 4. YÊU CẦU KỸ THUẬT & QUY CHUẨN ĐẦU RA (ACCEPTANCE CRITERIA)

1. **Chuẩn Kiến trúc 4 tầng (Layered Architecture):**
   - Nếu viết Backend: mỗi module phải phân chia rành mạch 4 tệp: `router.py` (API) -> `schemas.py` (Validate Pydantic v2) -> `service.py` (Logic nghiệp vụ) -> `models.py` (Bảng SQLAlchemy).
   - Logic kiểm tra điều kiện hoặc thuật toán phải nằm trong `service.py`, không viết logic trong `router.py`.
2. **Không sửa cấu trúc bảng Database tùy tiện:**
   - Sử dụng đúng 12 bảng đã định nghĩa trong `database/init_postgres.sql` và `docs/DATABASE_DESIGN.md`.
3. **Kiểm tra kỹ trước khi tạo PR:**
   - Chạy thử nghiệm Frontend: `npm run build` không được có lỗi syntax hoặc thiếu thư viện.
   - API trả về đúng cấu trúc chuẩn: `{ success: true, code: 200, message: "...", data: ... }`.
4. **Bảo mật:**
   - Tuyệt đối không lưu mật khẩu dạng văn bản thô (Plain text), bắt buộc băm qua Bcrypt.
   - Mọi API xử lý dữ liệu (ngoại trừ login) đều phải yêu cầu Bearer Token hợp lệ.
