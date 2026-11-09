# SMART-EDU LMS

**SMART-EDU LMS** là hệ thống quản lý đào tạo và vận hành trung tâm ngoại ngữ toàn diện theo mô hình hiện đại, tích hợp quản lý tuyển sinh trực tuyến, điều phối lớp học, kiểm soát sĩ số, lập lịch thời khóa biểu tự động phát hiện xung đột tài nguyên, quản lý sổ điểm trọng số chuẩn hóa và theo dõi lộ trình đào tạo học viên liên khóa.

Dự án được xây dựng theo kiến trúc tách rời (**Decoupled Architecture**) giữa **Frontend SPA** hiện đại và **Tầng Cơ sở dữ liệu** độc lập, tuân thủ nghiêm ngặt chuẩn thiết kế Modular Monolith DDD-Lite, sẵn sàng kết nối API linh hoạt với đa nền tảng backend.

---

## 📑 Mục lục

1. [Kiến trúc & Công nghệ sử dụng](#-kiến-trúc--công-nghệ-sử-dụng)
2. [Hệ thống giao diện & Luồng nghiệp vụ chính](#-hệ-thống-giao-diện--luồng-nghiệp-vụ-chính)
3. [Quy tắc nghiệp vụ & Ba thuật toán cốt lõi](#-quy-tắc-nghiệp-vụ--ba-thuật-toán-cốt-lõi)
4. [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
5. [Hướng dẫn cài đặt & Chạy phát triển (Quick Start)](#-hướng-dẫn-cài-đặt--chạy-phát-triển-quick-start)
6. [Quản trị Cơ sở dữ liệu & Seed Data](#-quản-trị-cơ-sở-dữ-liệu--seed-data)
7. [Chạy toàn bộ bằng Docker Compose](#-chạy-toàn-bộ-bằng-docker-compose)
8. [Kiểm tra & Xem dữ liệu Database](#-kiểm-tra--xem-dữ-liệu-database)
9. [Bảng tra cứu lệnh chung](#-bảng-tra-cứu-lệnh-chung)
10. [Cấu trúc thư mục & Tài liệu thiết kế](#-cấu-trúc-thư-mục--tài-liệu-thiết-kế)
11. [Xử lý lỗi thường gặp (Troubleshooting)](#-xử-lý-lỗi-thường-gặp-troubleshooting)

---

## 🛠 Kiến trúc & Công nghệ sử dụng

| Tầng (Layer) | Công nghệ chính | Vai trò trong dự án |
| --- | --- | --- |
| **Frontend (`frontend/`)** | React 19, Vite 8, Tailwind CSS v4, Axios, Lucide React | Giao diện SPA hiện đại theo chuẩn **Operate Mode** (tối ưu nhập liệu liên tục, `JetBrains Mono` + `tabular-nums` cho số liệu, Semantic Status Badges, Toast feedback không chặn luồng), quản lý phiên đăng nhập `AuthContext` và phân quyền RBAC 5 vai trò. |
| **Backend Specification (`docs/`)** | FastAPI, Python 3.11+, Pydantic v2, SQLAlchemy 2.0, Bcrypt, PyJWT | Đặc tả kiến trúc Modular Monolith DDD-Lite với 11 Bounded Contexts tự bao hàm (`router -> schema -> service -> model`), thực thi 3 thuật toán nghiệp vụ cốt lõi, bảo mật mật khẩu Bcrypt và xác thực JWT Bearer token 24h. |
| **Database (`database/` & `prisma/`)** | SQLite 3 (`language_center.db`), PostgreSQL 16, Prisma ORM 6 | Lưu trữ quan hệ chuẩn 3NF với 12 bảng thực thể. Hỗ trợ song song SQLite cục bộ (zero-config, có sẵn seed data) và PostgreSQL 16 container hóa sẵn sàng cho production. |
| **Hạ tầng & DevTools** | Docker Compose, Vite HMR, Prisma Studio | Môi trường container hóa dịch vụ database, script khởi động nhanh một chạm trên Windows (`start_frontend.bat`), trực quan hóa dữ liệu qua web UI Prisma Studio. |

---

## 🌿 Hệ thống giao diện & Luồng nghiệp vụ chính

### Các màn hình chức năng (Frontend Views & Routes)

Toàn bộ 11 phân hệ giao diện được tổ chức theo triết lý **Feature-Driven Architecture** trong `frontend/src/views/`:

| Phân hệ / Màn hình | View Component | Vai trò & Nghiệp vụ chi tiết |
| --- | --- | --- |
| **Xác thực & Hồ sơ** | `LoginView.jsx` | Đăng nhập hệ thống bằng tài khoản/mật khẩu băm Bcrypt, giải mã JWT Bearer token, tự động nhận diện 1 trong 5 vai trò (Admin, Staff, Teacher, Student, Parent). |
| **Quản trị Tài khoản** | `AccountsView.jsx` | Quản lý người dùng, phân quyền RBAC, cấp phát lại mật khẩu và khóa tài khoản vi phạm. |
| **Khóa học & Học phí** | `CoursesView.jsx` | Thiết lập chương trình đào tạo, thời lượng (tuần), biểu phí chuẩn và chuẩn đầu ra (Target Level). |
| **Hồ sơ Học viên** | `StudentsView.jsx` | Quản lý thông tin học viên, tra cứu lịch sử đào tạo, lớp đang theo học và gắn kết mã phụ huynh. |
| **Hồ sơ Giảng viên** | `TeachersView.jsx` | Danh sách giảng viên, chuyên môn đào tạo, liên kết lớp phụ trách và lịch giảng dạy. |
| **Điều phối Lớp học** | `ClassesView.jsx` | Quản lý danh sách lớp, ngày khai giảng/kết thúc, kiểm soát sĩ số thực tế (`enrolled/capacity`) và cảnh báo đầy lớp. |
| **Phòng học & Cơ sở** | `ClassroomsView.jsx` | Quản lý danh mục phòng học, sức chứa tối đa, trang thiết bị hỗ trợ và trạng thái sẵn sàng sử dụng. |
| **Tuyển sinh & Đăng ký** | `EnrollmentsView.jsx` | Tiếp nhận đơn đăng ký nhập học trực tuyến, xét duyệt học viên vào lớp hoặc từ chối kèm lý do phản hồi. |
| **Xếp lịch & TKB** | `SchedulesView.jsx` | Lập lịch thời khóa biểu từng buổi học, tích hợp thuật toán phát hiện va chạm lịch phòng học & giáo viên theo thời gian thực. |
| **Sổ điểm & Đánh giá** | `GradesView.jsx` | Bảng nhập điểm chi tiết (Chuyên cần, Giữa kỳ, Cuối kỳ), tự động tính điểm tổng kết theo trọng số, xếp loại và chốt khóa sổ điểm (`is_confirmed`). |
| **Cổng Phụ huynh & Lên khóa** | `ProgressionParentView.jsx` | Cổng thông tin phụ huynh tra cứu tiến độ con em, đồng thời thẩm định điều kiện tiên quyết để xét duyệt học viên nâng khóa học tiếp theo. |

---

## 📐 Quy tắc nghiệp vụ & Ba thuật toán cốt lõi

### 1. Thuật toán Phát hiện Xung đột Thời khóa biểu (Conflict Checker)
Khi xếp lịch ca học cho một buổi học (`session_date`), hệ thống kiểm tra điều kiện giao thoa khoảng thời gian:
```text
Va chạm lịch <=> (Start_A < End_B) VÀ (End_A > Start_B)
```
- **Ràng buộc kép:** Thuật toán quét đồng thời trên cả 2 tài nguyên trong cùng ngày học:
  1. **Phòng học (`classroom_id`):** Một phòng học không thể xếp 2 lớp khác nhau vào cùng một khung giờ.
  2. **Giảng viên (`teacher_id`):** Một giáo viên không thể đứng lớp tại 2 địa điểm/lớp khác nhau trong cùng thời điểm.
- Bất kỳ yêu cầu xếp lịch nào vi phạm sẽ bị từ chối ngay lập tức và đưa ra cảnh báo chính xác nguyên nhân xung đột.

### 2. Thuật toán Tính điểm Trọng số & Cơ chế Khóa sổ điểm (Grades Calculator)
Điểm số môn học được chuẩn hóa theo công thức trọng số đào tạo:
```text
Điểm tổng kết = (Chuyên cần x 0.2) + (Giữa kỳ x 0.3) + (Cuối kỳ x 0.5)
Xếp loại ĐẠT (PASSED) <=> (Điểm tổng kết >= 5.0) VÀ (Điểm cuối kỳ >= 4.0)
```
- **Cơ chế Khóa sổ (`is_confirmed = True`):** Sau khi giảng viên nhập điểm, nhân viên Học vụ tiến hành thẩm định và bấm **Khóa sổ điểm**. Khi đã khóa, toàn bộ quyền chỉnh sửa điểm của giảng viên bị đóng băng vĩnh viễn nhằm đảm bảo tính toàn vẹn dữ liệu.

### 3. Thuật toán Kiểm soát Điều kiện Tiên quyết Chuyển khóa (Progression Checker)
- Học viên chỉ đủ điều kiện đăng ký hoặc được chuyển tiếp lên khóa học kế tiếp trong lộ trình đào tạo khi khóa học tiên quyết đáp ứng đủ 2 tiêu chí bắt buộc:
  1. Trạng thái kết quả đạt **`PASSED`** (đạt cả điểm tổng kết và điểm sàn thi cuối kỳ).
  2. Sổ điểm của khóa học đó đã được nhân viên Học vụ **khóa sổ chính thức** (`is_confirmed = True`).

### 4. An ninh & Xác thực Hệ thống
- Mật khẩu người dùng được băm an toàn 1 chiều bằng thuật toán **Bcrypt** (Salt rounds = 12).
- Xác thực phiên làm việc thông qua **JSON Web Token (JWT)** chuẩn thuật toán `HS256`, thời hạn hiệu lực 24 giờ.
- Cơ chế bảo vệ tài khoản: Tự động khóa tài khoản tạm thời 15 phút nếu phát hiện nhập sai mật khẩu quá 5 lần liên tiếp.

---

## 💻 Yêu cầu hệ thống

- **Node.js:** Phiên bản `18.x` trở lên (Khuyên dùng `20+` LTS) và `npm`.
- **Cơ sở dữ liệu:** Tùy chọn 1 trong 2:
  - **SQLite 3:** Tích hợp sẵn trong repo, chạy ngay không cần cài đặt.
  - **Docker Desktop & Docker Compose:** Nếu muốn chạy PostgreSQL 16 container hóa.
- **Cổng mạng mặc định:**
  - Frontend SPA (React + Vite): `http://localhost:5173`
  - Prisma Studio GUI: `http://localhost:5555`
  - PostgreSQL Database (Docker): `localhost:5432`

---

## 🚀 Hướng dẫn cài đặt & Chạy phát triển (Quick Start)

Mở **PowerShell** hoặc **Terminal** tại thư mục gốc của dự án `SMART-EDU-VER2` và thực hiện:

### Bước 1: Cài đặt thư viện phụ thuộc Frontend

```powershell
cd frontend
npm install
```

### Bước 2: Khởi chạy ứng dụng Frontend (React 19)

```powershell
npm run dev
```

*(Trên môi trường Windows, bạn cũng có thể nhấp đúp trực tiếp vào tệp `start_frontend.bat` ở thư mục gốc để khởi chạy ứng dụng 1 chạm).*

### Bước 3: Truy cập hệ thống

- Mở trình duyệt và truy cập: **`http://localhost:5173`**
- Trải nghiệm giao diện quản trị đầy đủ của hệ thống.

---

## 🌱 Quản trị Cơ sở dữ liệu & Seed Data

Hệ thống hỗ trợ song song 2 tùy chọn lưu trữ dữ liệu quan hệ (12 bảng thực thể chuẩn 3NF):

### Tùy chọn A: Sử dụng SQLite (Mặc định — Zero Config)

Cơ sở dữ liệu SQLite đã được dựng sẵn và nạp dữ liệu mẫu tại:
`database/language_center.db`

- **Nội dung dữ liệu mẫu sẵn có:**
  - Danh mục người dùng thuộc đầy đủ 5 vai trò: `ADMIN`, `STAFF`, `TEACHER`, `STUDENT`, `PARENT`.
  - Danh mục khóa học chuẩn (IELTS, TOEIC, Giao tiếp), biểu phí và chuẩn đầu ra.
  - Danh sách phòng học, sức chứa và cơ sở vật chất.
  - Các lớp học đang vận hành, danh sách phân bổ học viên vào lớp và đơn đăng ký nhập học.
  - Lịch học mẫu không xung đột và bảng điểm kiểm thử công thức trọng số.
- Để tra cứu trực quan dữ liệu SQLite trên trình duyệt:
  ```powershell
  npm run prisma:sqlite:studio
  ```
  Trình duyệt mở tại: `http://localhost:5555`

### Tùy chọn B: Sử dụng PostgreSQL 16

Nếu muốn triển khai trên hệ quản trị cơ sở dữ liệu mạnh mẽ phục vụ production:
- Khởi động service qua Docker Compose (xem mục tiếp theo).
- File khởi tạo dữ liệu tự động: `database/init_postgres.sql` (chứa toàn bộ DDL tạo bảng, ràng buộc khóa ngoại, seed data và đồng bộ sequence khóa chính).

---

## 🐳 Chạy toàn bộ bằng Docker Compose

Dự án cung cấp cấu hình `docker-compose.yml` định nghĩa sẵn môi trường PostgreSQL 16 chính quy:

```powershell
docker compose up -d
docker compose ps
```

- **Cơ chế tự động:** Khi container khởi động lần đầu, Docker sẽ tự động mount tệp `database/init_postgres.sql` vào `/docker-entrypoint-initdb.d/`, tự động tạo toàn bộ bảng và nạp dữ liệu mẫu hoàn chỉnh.
- Dữ liệu được lưu trữ bền vững trong Docker volume `pgdata`. Lệnh `docker compose down` sẽ giải phóng tài nguyên mà không làm mất dữ liệu.

---

## 🗄 Kiểm tra & Xem dữ liệu Database

Bạn có thể kiểm tra trực tiếp dữ liệu cơ sở dữ liệu theo 3 phương thức:

1. **Dùng Prisma Studio (Giao diện Web trực quan — Khuyên dùng):**
   - Với SQLite:
     ```powershell
     npm run prisma:sqlite:studio
     ```
   - Với PostgreSQL:
     ```powershell
     npm run prisma:studio
     ```
   Trình duyệt mở tại **`http://localhost:5555`**, cho phép tra cứu, tìm kiếm và lọc dữ liệu trên cả 12 bảng thực thể.

2. **Dùng công cụ quản lý cơ sở dữ liệu chuyên dụng (DBeaver, TablePlus, DataGrip):**
   - **SQLite:** Mở trực tiếp tệp `database/language_center.db`.
   - **PostgreSQL 16:**
     - **Host:** `localhost` | **Port:** `5432`
     - **Database:** `language_center` | **Username:** `postgres` | **Password:** `postgrespassword2026`
     - **URL kết nối:** `postgresql://postgres:postgrespassword2026@localhost:5432/language_center?schema=public`

3. **Dùng dòng lệnh trong Docker container:**
   ```powershell
   docker compose exec db psql -U postgres -d language_center
   ```

---

## ⌨️ Bảng tra cứu lệnh chung

| Lệnh | Công dụng | Môi trường / Thư mục |
| --- | --- | --- |
| `npm run dev` | Khởi chạy máy chủ phát triển Frontend React 19 tại `http://localhost:5173` | Chạy tại `frontend/` |
| `npm run build` | Biên dịch tối ưu hóa mã nguồn Frontend để triển khai Production | Chạy tại `frontend/` |
| `npm run preview` | Chạy thử nghiệm bản build Production của Frontend cục bộ | Chạy tại `frontend/` |
| `docker compose up -d` | Khởi động container PostgreSQL 16 nền và tự động nạp `init_postgres.sql` | Chạy tại thư mục gốc |
| `docker compose down` | Dừng và hủy các container Docker cơ sở dữ liệu | Chạy tại thư mục gốc |
| `npm run prisma:sqlite:studio` | Mở giao diện Prisma Studio tra cứu Database SQLite tại `http://localhost:5555` | Chạy tại thư mục gốc |
| `npm run prisma:studio` | Mở giao diện Prisma Studio tra cứu Database PostgreSQL tại `http://localhost:5555` | Chạy tại thư mục gốc |
| `npm run prisma:seed` | Thực thi nạp lại dữ liệu mẫu thông qua Prisma Client Script | Chạy tại thư mục gốc |
| `start_frontend.bat` | Script nhấp đúp 1-click khởi chạy nhanh Frontend trên hệ điều hành Windows | Chạy tại thư mục gốc |

---

## 📂 Cấu trúc thư mục & Tài liệu thiết kế

```text
SMART-EDU-VER2/
├── frontend/                   # Ứng dụng Web Single Page Application (React 19 + Vite)
│   ├── src/
│   │   ├── components/         # Các UI component tái sử dụng (Navbar, Sidebar, Modal, DataTable)
│   │   ├── context/            # AuthContext (quản lý phiên & JWT), ToastContext (thông báo nổi)
│   │   ├── services/           # api.js tập trung gọi API qua Axios Interceptors
│   │   ├── views/              # 11 Views phân hệ nghiệp vụ tương ứng
│   │   ├── App.jsx             # Điều hướng router và bố cục ứng dụng theo phân quyền
│   │   └── main.jsx            # Entry point của React 19
│   ├── package.json            # Cấu hình dependencies (React 19, Tailwind v4, Lucide React)
│   └── vite.config.js          # Cấu hình Vite bundler & Dev server
├── database/                   # Module Cơ sở dữ liệu độc lập
│   ├── language_center.db      # CSDL SQLite binary nguyên bản (12 bảng + seed data sẵn)
│   ├── language_center_dump.sql# Bản xuất DDL & DML hoàn chỉnh theo chuẩn SQLite
│   ├── init_postgres.sql       # Script khởi tạo tự động tương thích PostgreSQL 16+
│   └── README.md               # Hướng dẫn chi tiết kỹ thuật CSDL
├── prisma/                     # Lược đồ ORM & Quản trị Migration
│   ├── schema.prisma           # Cấu hình lược đồ cho PostgreSQL
│   ├── schema.sqlite.prisma    # Cấu hình lược đồ cho SQLite cục bộ
│   └── seed.js                 # Script nạp dữ liệu mẫu đa nền tảng
├── docs/                       # Tài liệu thiết kế hệ thống chuyên sâu
│   ├── SYSTEM_DESIGN.md        # Thiết kế kiến trúc tổng thể, luồng nghiệp vụ & bảo mật
│   ├── DATABASE_DESIGN.md      # Chi tiết lược đồ ERD, quan hệ khóa ngoại và kiểu dữ liệu
│   ├── ISSUES.md               # Đặc tả 11 Core Business Issues & Tiêu chí nghiệm thu
│   └── DESIGN.md               # Nguyên lý thiết kế hướng đối tượng OOAD & DDD-Lite
├── .agents/                    # Bộ quy chuẩn Agent Skills & Workflow phát triển
├── docker-compose.yml          # Cấu hình dịch vụ PostgreSQL 16 container tự nạp init.sql
├── package.json                # Quản lý scripts Prisma toàn cục cho dự án
├── start_frontend.bat          # Script 1-click khởi chạy nhanh Frontend trên Windows
└── README.md                   # Tài liệu hướng dẫn sử dụng chính của dự án
```

**Nguyên tắc cấu trúc & Mở rộng:**
- Giao diện người dùng được phân tách triệt để giữa tầng trình diễn (`components/`), tầng điều hướng/trạng thái (`context/`, `App.jsx`) và tầng kết nối mạng (`services/api.js`).
- Toàn bộ 82 yêu cầu chức năng nghiệp vụ (FR-01 đến FR-82) và 11 Bounded Contexts đã được ánh xạ thành 11 GitHub Issues chính thức trên repository: [tenki1612/SMART-EDU-VER2/issues](https://github.com/tenki1612/SMART-EDU-VER2/issues).
- Bất kỳ dịch vụ Backend mới nào (FastAPI, Express, NestJS, Spring Boot) chỉ cần triển khai theo hợp đồng endpoints chuẩn trong `docs/SYSTEM_DESIGN.md` và `docs/ISSUES.md` là có thể tích hợp ngay lập tức với Frontend.

---

## 🔧 Xử lý lỗi thường gặp (Troubleshooting)

1. **Frontend không thể kết nối tới Backend API (`Network Error` / `401 Unauthorized`):**
   - Kiểm tra xem máy chủ backend API đã được khởi chạy hay chưa.
   - Kiểm tra cấu hình địa chỉ API trong `frontend/src/services/api.js` (mặc định trỏ đến `/api/v1` hoặc máy chủ trung gian).
   - Nếu bị lỗi xác thực 401, hãy đăng xuất và đăng nhập lại để hệ thống cập nhật JWT Bearer token mới vào `localStorage`.

2. **Lỗi xung đột cổng mạng (`EADDRINUSE` trên cổng `5173`, `5555` hoặc `5432`):**
   - Cổng `5173`: Đang có một ứng dụng Vite khác đang chạy. Bạn có thể tắt tiến trình cũ hoặc Vite sẽ tự động gợi ý chuyển sang cổng kế tiếp (ví dụ `http://localhost:5174`).
   - Cổng `5432`: Máy tính của bạn có thể đã cài sẵn PostgreSQL chạy dịch vụ nền (Windows Service). Hãy tạm dừng dịch vụ đó hoặc đổi cổng ánh xạ trong `docker-compose.yml` (ví dụ `"5433:5432"`).
   - Cổng `5555`: Prisma Studio cũ chưa được giải phóng. Nhấn `Ctrl + C` tại terminal đang chạy Prisma Studio để đóng kết nối.

3. **Lỗi không kết nối được PostgreSQL trong Docker:**
   - Đảm bảo Docker Desktop đã được bật và đang chạy.
   - Chạy lệnh `docker compose ps` để kiểm tra trạng thái container `smart-edu-db`. Nếu container gặp sự cố, kiểm tra log bằng lệnh `docker compose logs db`.

4. **Lỗi hiển thị ký tự tiếng Việt khi chạy scripts trên Windows Command Prompt:**
   - Chuyển mã hóa bảng mã dòng lệnh sang UTF-8 bằng cách chạy lệnh `chcp 65001` trước khi thực thi các lệnh terminal.

---

## 📄 Bản quyền & Thông tin tác giả

Dự án được xây dựng và phát triển phục vụ nghiên cứu, học tập và ứng dụng thực tiễn hệ thống Quản lý Đào tạo Ngoại ngữ.

- **Repository Chính:** [tenki1612/SMART-EDU-VER2](https://github.com/tenki1612/SMART-EDU-VER2)
- **Tác giả:** [tenki1612](https://github.com/tenki1612)
- **Giấy phép:** [MIT License](https://opensource.org/licenses/MIT)
