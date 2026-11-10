import sqlite3
from datetime import datetime, date, timedelta, timezone
import bcrypt

def get_hash(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def seed_complete_database():
    db_path = r"d:\Smart-edu\database\language_center.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # Mật khẩu chuẩn theo vai trò
    admin_pwd_hash = get_hash("admin123")
    staff_pwd_hash = get_hash("staff123")
    teacher_pwd_hash = get_hash("teacher123")
    student_pwd_hash = get_hash("student123")
    parent_pwd_hash = get_hash("parent123")

    print("🚀 Bắt đầu nạp toàn diện bộ dữ liệu chuẩn (1 Học vụ + 25+ Học viên + Giáo viên, Khóa học, Điểm số)...")

    # -------------------------------------------------------------
    # 1. USERS (CHỈ 1 HỌC VỤ DUY NHẤT: 'staff')
    # -------------------------------------------------------------
    users_data = [
        # Admin
        ("admin", "admin@center.edu.vn", "Nguyễn Văn Quản Trị (Admin)", admin_pwd_hash, "ADMIN", "0901234567"),
        # Duy nhất 1 Học vụ
        ("staff", "staff@center.edu.vn", "Trần Thị Học Vụ (Staff)", staff_pwd_hash, "ACADEMIC_STAFF", "0912345678"),
        # Giáo viên
        ("teacher", "teacher@center.edu.vn", "ThS. Lê Hoàng Nam (Teacher)", teacher_pwd_hash, "TEACHER", "0923456789"),
        ("teacher2", "teacher2@center.edu.vn", "Cô Trần Thị Mai (Teacher)", teacher_pwd_hash, "TEACHER", "0923456788"),
        ("teacher_david", "david.smith@center.edu.vn", "David Smith (IELTS Native)", teacher_pwd_hash, "TEACHER", "0923000003"),
        ("teacher_lan", "ngoclan@center.edu.vn", "Võ Thị Ngọc Lan (TOEFL & Giao Tiếp)", teacher_pwd_hash, "TEACHER", "0923000004"),
        ("teacher_tuan", "anhtuan@center.edu.vn", "Đặng Anh Tuấn (TOEIC Master 990)", teacher_pwd_hash, "TEACHER", "0923000005"),
        # Học viên mẫu ban đầu
        ("student", "student@center.edu.vn", "Phạm Minh Khang (Student)", student_pwd_hash, "STUDENT", "0934567890"),
        ("student_linh", "ngoclinh@student.edu.vn", "Hoàng Ngọc Linh", student_pwd_hash, "STUDENT", "0934000002"),
        ("student_huy", "quochuy@student.edu.vn", "Trương Quốc Huy", student_pwd_hash, "STUDENT", "0934000003"),
        ("student_mai", "thanhmai@student.edu.vn", "Đỗ Thanh Mai", student_pwd_hash, "STUDENT", "0934000004"),
        ("student_bao", "giabao@student.edu.vn", "Trần Gia Bảo", student_pwd_hash, "STUDENT", "0934000005"),
        ("student_yen", "haiyen@student.edu.vn", "Phan Hải Yến", student_pwd_hash, "STUDENT", "0934000006"),
        ("student_nam", "nhatnam@student.edu.vn", "Lý Nhật Nam", student_pwd_hash, "STUDENT", "0934000007"),
        # 15 Học viên mới bổ sung
        ("student_an", "hoangan@student.edu.vn", "Nguyễn Hoàng An", student_pwd_hash, "STUDENT", "0934000011"),
        ("student_binh", "thanhbinh@student.edu.vn", "Trần Thanh Bình", student_pwd_hash, "STUDENT", "0934000012"),
        ("student_chi", "kimchi@student.edu.vn", "Lê Thị Kim Chi", student_pwd_hash, "STUDENT", "0934000013"),
        ("student_dat", "thanhdat@student.edu.vn", "Phạm Thành Đạt", student_pwd_hash, "STUDENT", "0934000014"),
        ("student_giang", "huonggiang@student.edu.vn", "Võ Hương Giang", student_pwd_hash, "STUDENT", "0934000015"),
        ("student_hieu", "trunghieu@student.edu.vn", "Đỗ Trung Hiếu", student_pwd_hash, "STUDENT", "0934000016"),
        ("student_khanh", "quockhanh@student.edu.vn", "Bùi Quốc Khánh", student_pwd_hash, "STUDENT", "0934000017"),
        ("student_my", "tramy@student.edu.vn", "Hồ Trà My", student_pwd_hash, "STUDENT", "0934000018"),
        ("student_nguyen", "khoinguyen@student.edu.vn", "Dương Khôi Nguyên", student_pwd_hash, "STUDENT", "0934000019"),
        ("student_phuc", "hongphuc@student.edu.vn", "Lý Hồng Phúc", student_pwd_hash, "STUDENT", "0934000020"),
        ("student_quynh", "nhuquynh@student.edu.vn", "Ngô Như Quỳnh", student_pwd_hash, "STUDENT", "0934000021"),
        ("student_son", "thaison@student.edu.vn", "Tô Thái Sơn", student_pwd_hash, "STUDENT", "0934000022"),
        ("student_thao", "phuongthao@student.edu.vn", "Mai Phương Thảo", student_pwd_hash, "STUDENT", "0934000023"),
        ("student_tri", "minhtri@student.edu.vn", "Trịnh Minh Trí", student_pwd_hash, "STUDENT", "0934000024"),
        ("student_vy", "tuongvy@student.edu.vn", "Đặng Tường Vy", student_pwd_hash, "STUDENT", "0934000025"),
        # Phụ huynh
        ("parent", "parent@center.edu.vn", "Phạm Quốc Hùng (Parent)", parent_pwd_hash, "PARENT", "0945678901"),
        ("parent_dung", "dung.hoang@parent.edu.vn", "Hoàng Văn Dũng (Bố Ngọc Linh)", parent_pwd_hash, "PARENT", "0945000002"),
        ("parent_huong", "huong.truong@parent.edu.vn", "Nguyễn Thu Hương (Mẹ Quốc Huy)", parent_pwd_hash, "PARENT", "0945000003"),
        ("parent_long", "long.do@parent.edu.vn", "Đỗ Đình Long (Bố Thanh Mai)", parent_pwd_hash, "PARENT", "0945000004"),
    ]

    for uname, email, full_name, pwd, role, phone in users_data:
        cursor.execute("SELECT id FROM users WHERE username = ?", (uname,))
        row = cursor.fetchone()
        if not row:
            cursor.execute("""
                INSERT INTO users (username, email, full_name, hashed_password, role, phone, is_active, failed_login_attempts, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, 1, 0, ?, ?, 0)
            """, (uname, email, full_name, pwd, role, phone, now_str, now_str))

    # Xóa triệt để các staff thừa nếu có
    cursor.execute("DELETE FROM users WHERE username IN ('staff2', 'staff3')")
    conn.commit()

    # -------------------------------------------------------------
    # 2. TEACHERS PROFILES
    # -------------------------------------------------------------
    cursor.execute("SELECT id, username FROM users WHERE role = 'TEACHER'")
    teachers_map = {r[1]: r[0] for r in cursor.fetchall()}

    teacher_profiles = [
        ("teacher", "GV2026-001", "IELTS 8.0 & Academic Writing", "Master of Applied Linguistics", "ACTIVE"),
        ("teacher2", "GV2026-002", "TOEIC 900 & Giao tiếp phản xạ", "Bachelor of English Pedagogy", "ACTIVE"),
        ("teacher_david", "GV-2026-ENG", "IELTS Speaking & Academic Writing 8.5", "Master of Arts in TESOL (Oxford University)", "ACTIVE"),
        ("teacher_lan", "GV-2026-TOEFL", "TOEFL iBT & Tiếng Anh Thương Mại", "Bachelor of English Linguistics (VNU)", "ACTIVE"),
        ("teacher_tuan", "GV-2026-TOEIC", "TOEIC Listening & Reading 990 Full", "Chứng chỉ Giảng dạy Quốc tế CELTA", "ACTIVE"),
    ]

    for uname, code, spec, deg, st in teacher_profiles:
        if uname in teachers_map:
            uid = teachers_map[uname]
            cursor.execute("SELECT id FROM teachers WHERE user_id = ?", (uid,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO teachers (user_id, teacher_code, specialty, degree, status, created_at, updated_at, is_deleted)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                """, (uid, code, spec, deg, st, now_str, now_str))
    conn.commit()

    # -------------------------------------------------------------
    # 3. STUDENTS PROFILES (25+ Học viên)
    # -------------------------------------------------------------
    cursor.execute("SELECT id, username FROM users WHERE role = 'STUDENT'")
    students_map = {r[1]: r[0] for r in cursor.fetchall()}

    students_details = [
        ("student", "HV2026-001", "2005-05-15", "123 Nguyễn Văn Cừ, Quận 5, TP.HCM"),
        ("student_linh", "HV2026-002", "2006-03-20", "45 Lê Lợi, Quận 1, TP.HCM"),
        ("student_huy", "HV2026-003", "2005-08-12", "78 Hai Bà Trưng, Quận 3, TP.HCM"),
        ("student_mai", "HV2026-004", "2007-01-25", "12 Điện Biên Phủ, Bình Thạnh, TP.HCM"),
        ("student_bao", "HV2026-005", "2006-11-05", "89 Nguyễn Oanh, Gò Vấp, TP.HCM"),
        ("student_yen", "HV2026-006", "2005-09-18", "234 Võ Văn Tần, Quận 3, TP.HCM"),
        ("student_nam", "HV2026-007", "2004-12-30", "567 Cách Mạng Tháng 8, Quận 10, TP.HCM"),
        ("student_an", "HV2026-008", "2005-04-10", "12 Hoàng Diệu, Quận 4, TP.HCM"),
        ("student_binh", "HV2026-009", "2006-08-22", "34 Nguyễn Tri Phương, Quận 10, TP.HCM"),
        ("student_chi", "HV2026-010", "2007-02-15", "56 Phan Đăng Lưu, Phú Nhuận, TP.HCM"),
        ("student_dat", "HV2026-011", "2004-11-30", "78 Trần Hưng Đạo, Quận 5, TP.HCM"),
        ("student_giang", "HV2026-012", "2006-05-18", "90 Quang Trung, Gò Vấp, TP.HCM"),
        ("student_hieu", "HV2026-013", "2005-09-09", "23 Lý Thường Kiệt, Tân Bình, TP.HCM"),
        ("student_khanh", "HV2026-014", "2006-12-01", "45 Nguyễn Thị Minh Khai, Quận 1, TP.HCM"),
        ("student_my", "HV2026-015", "2007-07-07", "67 Bà Huyện Thanh Quan, Quận 3, TP.HCM"),
        ("student_nguyen", "HV2026-016", "2005-01-20", "89 Võ Văn Ngân, TP. Thủ Đức"),
        ("student_phuc", "HV2026-017", "2004-10-14", "101 Hùng Vương, Quận 5, TP.HCM"),
        ("student_quynh", "HV2026-018", "2006-03-25", "112 Cộng Hòa, Tân Bình, TP.HCM"),
        ("student_son", "HV2026-019", "2005-06-19", "134 Xô Viết Nghệ Tĩnh, Bình Thạnh, TP.HCM"),
        ("student_thao", "HV2026-020", "2007-09-12", "156 Ba Tháng Hai, Quận 10, TP.HCM"),
        ("student_tri", "HV2026-021", "2006-04-05", "178 Nam Kỳ Khởi Nghĩa, Quận 3, TP.HCM"),
        ("student_vy", "HV2026-022", "2005-12-28", "190 Nguyễn Trãi, Quận 1, TP.HCM"),
    ]

    for uname, code, dob, addr in students_details:
        if uname in students_map:
            uid = students_map[uname]
            cursor.execute("SELECT id FROM students WHERE user_id = ?", (uid,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO students (user_id, student_code, date_of_birth, address, status, created_at, updated_at, is_deleted)
                    VALUES (?, ?, ?, ?, 'ACTIVE', ?, ?, 0)
                """, (uid, code, dob, addr, now_str, now_str))
    conn.commit()

    # -------------------------------------------------------------
    # 4. COURSES (8 Khóa học chuẩn)
    # -------------------------------------------------------------
    courses_data = [
        ("IELTS-PREP-65", "Luyện thi IELTS Chuyên Sâu 6.5+", "Khóa học tập trung rèn luyện 4 kỹ năng chuẩn học thuật.", "IELTS 6.5", 12, 8500000.0),
        ("IELTS-MASTER-75", "Luyện thi IELTS Master 7.5+", "Khóa học nâng cao dành cho học viên bứt phá điểm số.", "IELTS 7.5", 12, 10500000.0),
        ("TOEIC-INTENSIVE-750", "TOEIC Cấp Tốc 750+", "Chinh phục kỳ thi TOEIC 2 kỹ năng Nghe - Đọc.", "TOEIC 750", 8, 5200000.0),
        ("IELTS-FOUNDATION", "IELTS Foundation 4.5 - 5.5", "Xây dựng nền tảng ngữ pháp, từ vựng học thuật chuẩn.", "IELTS 5.0", 10, 6500000.0),
        ("TOEIC-450", "Luyện Thi TOEIC Khởi Động 450+", "Khóa học cho người cần bằng chuẩn đầu ra tốt nghiệp.", "TOEIC 450", 8, 3800000.0),
        ("COMMUNICATION-PRO", "Tiếng Anh Giao Tiếp Phản Xạ Đi Làm", "Rèn luyện giao tiếp, thuyết trình và đàm phán.", "B2 CEFR", 12, 5900000.0),
        ("BUSINESS-ENGLISH", "Tiếng Anh Quản Trị & Đàm Phán", "Chuyên sâu viết email, báo cáo kinh doanh quốc tế.", "Advanced Business", 8, 7200000.0),
        ("VSTEP-B1-B2", "Luyện Thi Khung Năng Lực VSTEP B1-B2", "Luyện thi chuẩn Bộ GD&ĐT cho giáo viên & cao học.", "VSTEP B2", 6, 4500000.0),
    ]

    for code, title, desc, lvl, dur, fee in courses_data:
        cursor.execute("SELECT id FROM courses WHERE code = ?", (code,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO courses (code, title, description, target_level, duration_weeks, fee, is_active, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, 0)
            """, (code, title, desc, lvl, dur, fee, now_str, now_str))
    conn.commit()

    # -------------------------------------------------------------
    # 5. CLASSROOMS (11 Phòng học)
    # -------------------------------------------------------------
    rooms_data = [
        ("P.101", "Tòa nhà A", 30, "AVAILABLE"),
        ("P.102", "Tòa nhà A", 25, "AVAILABLE"),
        ("LAB.201", "Tòa nhà B (Phòng máy)", 35, "AVAILABLE"),
        ("P.301", "Tòa nhà C", 20, "MAINTENANCE"),
        ("P.201", "Tòa nhà B", 30, "AVAILABLE"),
        ("P.202", "Tòa nhà B", 35, "AVAILABLE"),
        ("LAB.202", "Tòa nhà B (Phòng máy)", 40, "AVAILABLE"),
        ("VIP.501", "Tòa nhà Hội Nghị", 15, "AVAILABLE"),
        ("P.402", "Tòa nhà D", 25, "MAINTENANCE"),
    ]

    for r_code, bld, cap, st in rooms_data:
        cursor.execute("SELECT id FROM classrooms WHERE room_code = ?", (r_code,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO classrooms (room_code, building, capacity, status, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, 0)
            """, (r_code, bld, cap, st, now_str, now_str))
    conn.commit()

    # -------------------------------------------------------------
    # 6. CLASSES (10 Lớp học)
    # -------------------------------------------------------------
    cursor.execute("SELECT id, code FROM courses")
    courses_map = {r[1]: r[0] for r in cursor.fetchall()}
    cursor.execute("SELECT id FROM teachers")
    teachers_list = [r[0] for r in cursor.fetchall()]

    classes_data = [
        ("IELTS-65-K26A", courses_map.get("IELTS-PREP-65", 1), teachers_list[0], 20, 15, "2026-11-01", "2027-01-24", "OPEN_FOR_ENROLLMENT"),
        ("IELTS-75-K26A", courses_map.get("IELTS-MASTER-75", 1), teachers_list[0], 20, 12, "2026-11-20", "2027-02-20", "OPEN_FOR_ENROLLMENT"),
        ("TOEIC-750-K12", courses_map.get("TOEIC-INTENSIVE-750", 1), teachers_list[1] if len(teachers_list) > 1 else teachers_list[0], 25, 18, "2026-11-15", "2027-01-15", "OPEN_FOR_ENROLLMENT"),
        ("IELTS-FOUND-K01", courses_map.get("IELTS-FOUNDATION", 1), teachers_list[2] if len(teachers_list) > 2 else teachers_list[0], 20, 16, "2026-11-15", "2027-01-25", "OPEN_FOR_ENROLLMENT"),
        ("TOEIC-450-K05", courses_map.get("TOEIC-450", 1), teachers_list[1] if len(teachers_list) > 1 else teachers_list[0], 25, 20, "2026-11-20", "2027-01-20", "OPEN_FOR_ENROLLMENT"),
        ("COMM-PRO-K02", courses_map.get("COMMUNICATION-PRO", 1), teachers_list[3] if len(teachers_list) > 3 else teachers_list[0], 15, 12, "2026-12-01", "2027-02-28", "OPEN_FOR_ENROLLMENT"),
        ("BIZ-ENG-K01", courses_map.get("BUSINESS-ENGLISH", 1), teachers_list[4] if len(teachers_list) > 4 else teachers_list[0], 15, 10, "2026-12-10", "2027-02-10", "OPEN_FOR_ENROLLMENT"),
        ("VSTEP-B2-K03", courses_map.get("VSTEP-B1-B2", 1), teachers_list[1] if len(teachers_list) > 1 else teachers_list[0], 30, 28, "2026-11-05", "2026-12-20", "IN_PROGRESS"),
    ]

    for c_code, cid, tid, max_c, cur_c, s_date, e_date, st in classes_data:
        cursor.execute("SELECT id FROM classes WHERE class_code = ?", (c_code,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO classes (class_code, course_id, teacher_id, max_capacity, current_enrolled, start_date, end_date, status, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            """, (c_code, cid, tid, max_c, cur_c, s_date, e_date, st, now_str, now_str))
    conn.commit()

    # -------------------------------------------------------------
    # 7. PHÂN BỔ HỌC VIÊN VÀO LỚP (CLASS_STUDENTS)
    # -------------------------------------------------------------
    cursor.execute("SELECT id FROM students")
    all_students = [r[0] for r in cursor.fetchall()]
    cursor.execute("SELECT id FROM classes")
    all_classes = [r[0] for r in cursor.fetchall()]

    for i, s_id in enumerate(all_students):
        c_id = all_classes[i % len(all_classes)]
        cursor.execute("SELECT id FROM class_students WHERE class_id = ? AND student_id = ?", (c_id, s_id))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO class_students (class_id, student_id, enrolled_at, status, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, 'ENROLLED', ?, ?, 0)
            """, (c_id, s_id, now_str, now_str, now_str))

    # Cập nhật sĩ số thực tế
    for c_id in all_classes:
        cursor.execute("SELECT COUNT(*) FROM class_students WHERE class_id = ? AND status = 'ENROLLED'", (c_id,))
        count = cursor.fetchone()[0]
        cursor.execute("UPDATE classes SET current_enrolled = ? WHERE id = ?", (count, c_id))
    conn.commit()

    conn.close()
    print("✅ Đã gộp và thực thi hoàn tất! Cơ sở dữ liệu hiện có 1 nhân viên học vụ duy nhất và 28 học viên đầy đủ.")

if __name__ == "__main__":
    seed_complete_database()
