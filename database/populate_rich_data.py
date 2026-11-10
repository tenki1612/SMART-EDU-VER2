import sqlite3
from datetime import datetime, date, timedelta, timezone
import bcrypt

def get_hash(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def populate_rich_data():
    conn = sqlite3.connect(r"d:\Smart-edu\database\language_center.db")
    cursor = conn.cursor()

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    pwd_hash = get_hash("123456") # Mật khẩu chung chuẩn 123456 cho các tài khoản mới thêm
    admin_pwd_hash = get_hash("admin123")
    teacher_pwd_hash = get_hash("teacher123")
    student_pwd_hash = get_hash("student123")
    parent_pwd_hash = get_hash("parent123")
    staff_pwd_hash = get_hash("staff123")

    print("🚀 Bắt đầu bổ sung dữ liệu đa dạng cho 12 bảng...")

    # 1. Thêm Users mới
    new_users = [
        # Staff mới
        ("staff2", "staff2@center.edu.vn", "Nguyễn Văn Đức (Tư Vấn Tuyển Sinh)", staff_pwd_hash, "ACADEMIC_STAFF", "0912000002", True),
        ("staff3", "staff3@center.edu.vn", "Lê Thị Bích Ngọc (Quản Lý Học Vụ)", staff_pwd_hash, "ACADEMIC_STAFF", "0912000003", True),
        # Teachers mới
        ("teacher_david", "david.smith@center.edu.vn", "David Smith (IELTS Native)", teacher_pwd_hash, "TEACHER", "0923000003", True),
        ("teacher_lan", "ngoclan@center.edu.vn", "Võ Thị Ngọc Lan (TOEFL & Giao Tiếp)", teacher_pwd_hash, "TEACHER", "0923000004", True),
        ("teacher_tuan", "anhtuan@center.edu.vn", "Đặng Anh Tuấn (TOEIC Master 990)", teacher_pwd_hash, "TEACHER", "0923000005", True),
        # Students mới
        ("student_linh", "ngoclinh@student.edu.vn", "Hoàng Ngọc Linh", student_pwd_hash, "STUDENT", "0934000002", True),
        ("student_huy", "quochuy@student.edu.vn", "Trương Quốc Huy", student_pwd_hash, "STUDENT", "0934000003", True),
        ("student_mai", "thanhmai@student.edu.vn", "Đỗ Thanh Mai", student_pwd_hash, "STUDENT", "0934000004", True),
        ("student_bao", "giabao@student.edu.vn", "Trần Gia Bảo", student_pwd_hash, "STUDENT", "0934000005", True),
        ("student_yen", "haiyen@student.edu.vn", "Phan Hải Yến", student_pwd_hash, "STUDENT", "0934000006", True),
        ("student_nam", "nhatnam@student.edu.vn", "Lý Nhật Nam", student_pwd_hash, "STUDENT", "0934000007", True),
        # Parents mới
        ("parent_dung", "dung.hoang@parent.edu.vn", "Hoàng Văn Dũng (Bố Ngọc Linh)", parent_pwd_hash, "PARENT", "0945000002", True),
        ("parent_huong", "huong.truong@parent.edu.vn", "Nguyễn Thu Hương (Mẹ Quốc Huy)", parent_pwd_hash, "PARENT", "0945000003", True),
        ("parent_long", "long.do@parent.edu.vn", "Đỗ Đình Long (Bố Thanh Mai)", parent_pwd_hash, "PARENT", "0945000004", True),
    ]

    for u in new_users:
        cursor.execute("SELECT id FROM users WHERE username = ?", (u[0],))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO users (username, email, full_name, hashed_password, role, phone, is_active, failed_login_attempts, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?, ?, 0)
            """, (u[0], u[1], u[2], u[3], u[4], u[5], u[6], now_str, now_str))

    conn.commit()

    # 2. Thêm Profiles cho Giáo viên
    cursor.execute("SELECT id, username FROM users WHERE role = 'TEACHER'")
    teachers_map = {row[1]: row[0] for row in cursor.fetchall()}

    teacher_profiles_data = [
        ("teacher_david", "GV-2026-ENG", "IELTS Speaking & Academic Writing 8.5", "Master of Arts in TESOL (Oxford University)", "ACTIVE"),
        ("teacher_lan", "GV-2026-TOEFL", "TOEFL iBT & Tiếng Anh Thương Mại (Business English)", "Bachelor of English Linguistics (VNU)", "ACTIVE"),
        ("teacher_tuan", "GV-2026-TOEIC", "TOEIC Listening & Reading 990 Full", "Chứng chỉ Giảng dạy Quốc tế CELTA", "ACTIVE"),
    ]

    for uname, code, spec, deg, st in teacher_profiles_data:
        if uname in teachers_map:
            uid = teachers_map[uname]
            cursor.execute("SELECT id FROM teachers WHERE user_id = ?", (uid,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO teachers (user_id, teacher_code, specialty, degree, status, created_at, updated_at, is_deleted)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                """, (uid, code, spec, deg, st, now_str, now_str))

    conn.commit()

    # 3. Thêm Profiles cho Học viên
    cursor.execute("SELECT id, username FROM users WHERE role = 'STUDENT'")
    students_map = {row[1]: row[0] for row in cursor.fetchall()}

    student_profiles_data = [
        ("student_linh", "HV2026-002", "2006-03-20", "45 Lê Lợi, Quận 1, TP.HCM"),
        ("student_huy", "HV2026-003", "2005-08-12", "78 Hai Bà Trưng, Quận 3, TP.HCM"),
        ("student_mai", "HV2026-004", "2007-01-25", "12 Điện Biên Phủ, Bình Thạnh, TP.HCM"),
        ("student_bao", "HV2026-005", "2006-11-05", "89 Nguyễn Oanh, Gò Vấp, TP.HCM"),
        ("student_yen", "HV2026-006", "2005-09-18", "234 Võ Văn Tần, Quận 3, TP.HCM"),
        ("student_nam", "HV2026-007", "2004-12-30", "567 Cách Mạng Tháng 8, Quận 10, TP.HCM"),
    ]

    for uname, code, dob, addr in student_profiles_data:
        if uname in students_map:
            uid = students_map[uname]
            cursor.execute("SELECT id FROM students WHERE user_id = ?", (uid,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO students (user_id, student_code, date_of_birth, address, status, created_at, updated_at, is_deleted)
                    VALUES (?, ?, ?, ?, 'ACTIVE', ?, ?, 0)
                """, (uid, code, dob, addr, now_str, now_str))

    conn.commit()

    # 4. Thêm Khóa học mới đa dạng
    courses_data = [
        ("IELTS-FOUNDATION", "IELTS Foundation 4.5 - 5.5", "Xây dựng nền tảng ngữ pháp, từ vựng học thuật và phát âm chuẩn quốc tế.", "IELTS 5.0", 10, 6500000.0),
        ("TOEIC-450", "Luyện Thi TOEIC Khởi Động 450+", "Khóa học dành cho người mất gốc tiếng Anh cần bằng chuẩn đầu ra tốt nghiệp.", "TOEIC 450", 8, 3800000.0),
        ("COMMUNICATION-PRO", "Tiếng Anh Giao Tiếp Phản Xạ Đi Làm", "Rèn luyện giao tiếp thương mại, thuyết trình và đàm phán trong môi trường đa quốc gia.", "B2 CEFR", 12, 5900000.0),
        ("BUSINESS-ENGLISH", "Tiếng Anh Chuyên Ngành Quản Trị & Đàm Phán", "Chuyên sâu viết email, báo cáo tài chính và thuật ngữ kinh doanh quốc tế.", "Advanced Business", 8, 7200000.0),
        ("VSTEP-B1-B2", "Luyện Thi Khung Năng Lực VSTEP B1-B2", "Khóa luyện thi cấp tốc chuẩn Bộ Giáo Dục & Đào Tạo dành cho giáo viên và cao học.", "VSTEP B2", 6, 4500000.0),
    ]

    for code, title, desc, lvl, dur, fee in courses_data:
        cursor.execute("SELECT id FROM courses WHERE code = ?", (code,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO courses (code, title, description, target_level, duration_weeks, fee, is_active, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, 0)
            """, (code, title, desc, lvl, dur, fee, now_str, now_str))

    conn.commit()

    # 5. Thêm Phòng học mới
    classrooms_data = [
        ("P.201", "Tòa nhà B", 30, "AVAILABLE"),
        ("P.202", "Tòa nhà B", 35, "AVAILABLE"),
        ("LAB.202", "Tòa nhà B (Phòng máy)", 40, "AVAILABLE"),
        ("VIP.501", "Tòa nhà Hội Nghị", 15, "AVAILABLE"),
        ("P.402", "Tòa nhà D", 25, "MAINTENANCE"),
    ]

    for r_code, bld, cap, st in classrooms_data:
        cursor.execute("SELECT id FROM classrooms WHERE room_code = ?", (r_code,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO classrooms (room_code, building, capacity, status, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, 0)
            """, (r_code, bld, cap, st, now_str, now_str))

    conn.commit()

    # 6. Thêm Lớp học mới
    cursor.execute("SELECT id, code FROM courses")
    courses_map = {row[1]: row[0] for row in cursor.fetchall()}
    cursor.execute("SELECT id, user_id FROM teachers")
    teachers_list = [row[0] for row in cursor.fetchall()]

    classes_data = [
        ("IELTS-FOUND-K01", courses_map.get("IELTS-FOUNDATION", 1), teachers_list[0] if teachers_list else 1, 20, 15, "2026-11-15", "2027-01-25", "OPEN_FOR_ENROLLMENT"),
        ("TOEIC-450-K05", courses_map.get("TOEIC-450", 1), teachers_list[1] if len(teachers_list) > 1 else 1, 25, 20, "2026-11-20", "2027-01-20", "OPEN_FOR_ENROLLMENT"),
        ("COMM-PRO-K02", courses_map.get("COMMUNICATION-PRO", 1), teachers_list[2] if len(teachers_list) > 2 else 1, 15, 12, "2026-12-01", "2027-02-28", "OPEN_FOR_ENROLLMENT"),
        ("BIZ-ENG-K01", courses_map.get("BUSINESS-ENGLISH", 1), teachers_list[0] if teachers_list else 1, 15, 8, "2026-12-10", "2027-02-10", "OPEN_FOR_ENROLLMENT"),
        ("VSTEP-B2-K03", courses_map.get("VSTEP-B1-B2", 1), teachers_list[1] if len(teachers_list) > 1 else 1, 30, 28, "2026-11-05", "2026-12-20", "IN_PROGRESS"),
    ]

    for c_code, cid, tid, max_c, cur_c, s_date, e_date, st in classes_data:
        cursor.execute("SELECT id FROM classes WHERE class_code = ?", (c_code,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO classes (class_code, course_id, teacher_id, max_capacity, current_enrolled, start_date, end_date, status, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            """, (c_code, cid, tid, max_c, cur_c, s_date, e_date, st, now_str, now_str))

    conn.commit()

    # 7. Thêm Quan hệ Phụ huynh - Học viên (Parent-Student)
    cursor.execute("SELECT id, username FROM users WHERE role = 'PARENT'")
    parents_map = {row[1]: row[0] for row in cursor.fetchall()}
    cursor.execute("SELECT id, student_code FROM students")
    students_code_map = {row[1]: row[0] for row in cursor.fetchall()}

    parent_links_data = [
        ("parent_dung", "HV2026-002", "Bố ruột"),
        ("parent_huong", "HV2026-003", "Mẹ ruột"),
        ("parent_long", "HV2026-004", "Bố ruột"),
    ]

    for p_user, s_code, rel in parent_links_data:
        if p_user in parents_map and s_code in students_code_map:
            p_id = parents_map[p_user]
            s_id = students_code_map[s_code]
            cursor.execute("SELECT id FROM parent_students WHERE parent_user_id = ? AND student_id = ?", (p_id, s_id))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO parent_students (parent_user_id, student_id, relationship_type, created_at, updated_at, is_deleted)
                    VALUES (?, ?, ?, ?, ?, 0)
                """, (p_id, s_id, rel, now_str, now_str))

    conn.commit()

    # 8. Thêm Học viên vào Lớp (ClassStudent)
    cursor.execute("SELECT id FROM students")
    all_student_ids = [r[0] for r in cursor.fetchall()]
    cursor.execute("SELECT id FROM classes")
    all_class_ids = [r[0] for r in cursor.fetchall()]

    for i, s_id in enumerate(all_student_ids):
        c_id = all_class_ids[i % len(all_class_ids)]
        cursor.execute("SELECT id FROM class_students WHERE class_id = ? AND student_id = ?", (c_id, s_id))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO class_students (class_id, student_id, enrolled_at, status, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, 'ENROLLED', ?, ?, 0)
            """, (c_id, s_id, now_str, now_str, now_str))

    conn.commit()

    # 9. Thêm Đơn đăng ký ghi danh (Enrollment Requests)
    enrollment_data = [
        (all_student_ids[0], all_class_ids[0], "APPROVED", "Đã thanh toán học phí qua VNPAY", 2),
        (all_student_ids[1] if len(all_student_ids) > 1 else 1, all_class_ids[1] if len(all_class_ids) > 1 else 1, "APPROVED", "Học viên được duyệt học bổng 20%", 2),
        (all_student_ids[2] if len(all_student_ids) > 2 else 1, all_class_ids[2] if len(all_class_ids) > 2 else 1, "PENDING", "Chờ kiểm tra đầu vào trực tiếp", None),
        (all_student_ids[3] if len(all_student_ids) > 3 else 1, all_class_ids[0], "PENDING", "Đăng ký ca tối thứ 2-4-6", None),
        (all_student_ids[4] if len(all_student_ids) > 4 else 1, all_class_ids[1] if len(all_class_ids) > 1 else 1, "REJECTED", "Không đáp ứng điểm sàn đầu vào khóa Master", 2),
    ]

    for s_id, c_id, st, note, rev_by in enrollment_data:
        cursor.execute("""
            INSERT INTO enrollment_requests (student_id, class_id, request_date, status, note, reviewed_by, reviewed_at, created_at, updated_at, is_deleted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (s_id, c_id, now_str, st, note, rev_by, now_str if rev_by else None, now_str, now_str))

    conn.commit()

    # 10. Thêm Thời khóa biểu (Schedule Sessions)
    cursor.execute("SELECT id FROM classrooms")
    all_rooms = [r[0] for r in cursor.fetchall()]

    today = date.today()
    schedules_data = [
        (all_class_ids[0], all_rooms[0], teachers_list[0] if teachers_list else 1, today + timedelta(days=1), "18:00", "20:00", "Ca 3 (18:00 - 20:00)", 1, "SCHEDULED"),
        (all_class_ids[0], all_rooms[0], teachers_list[0] if teachers_list else 1, today + timedelta(days=3), "18:00", "20:00", "Ca 3 (18:00 - 20:00)", 1, "SCHEDULED"),
        (all_class_ids[0], all_rooms[0], teachers_list[0] if teachers_list else 1, today + timedelta(days=5), "18:00", "20:00", "Ca 3 (18:00 - 20:00)", 1, "SCHEDULED"),
        (all_class_ids[1] if len(all_class_ids) > 1 else 1, all_rooms[1] if len(all_rooms) > 1 else 1, teachers_list[1] if len(teachers_list) > 1 else 1, today + timedelta(days=2), "08:00", "10:00", "Ca 1 (08:00 - 10:00)", 1, "SCHEDULED"),
        (all_class_ids[1] if len(all_class_ids) > 1 else 1, all_rooms[1] if len(all_rooms) > 1 else 1, teachers_list[1] if len(teachers_list) > 1 else 1, today + timedelta(days=4), "08:00", "10:00", "Ca 1 (08:00 - 10:00)", 1, "SCHEDULED"),
        (all_class_ids[2] if len(all_class_ids) > 2 else 1, all_rooms[2] if len(all_rooms) > 2 else 1, teachers_list[2] if len(teachers_list) > 2 else 1, today + timedelta(days=2), "14:00", "16:00", "Ca 2 (14:00 - 16:00)", 1, "SCHEDULED"),
        (all_class_ids[2] if len(all_class_ids) > 2 else 1, all_rooms[2] if len(all_rooms) > 2 else 1, teachers_list[2] if len(teachers_list) > 2 else 1, today + timedelta(days=6), "14:00", "16:00", "Ca 2 (14:00 - 16:00)", 1, "SCHEDULED"),
    ]

    for c_id, r_id, t_id, s_date, st_time, end_time, slot, is_conf, st in schedules_data:
        cursor.execute("""
            INSERT INTO schedule_sessions (class_id, classroom_id, teacher_id, session_date, start_time, end_time, slot_name, is_confirmed, status, created_at, updated_at, is_deleted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (c_id, r_id, t_id, s_date, st_time, end_time, slot, is_conf, st, now_str, now_str))

    conn.commit()

    # 11. Thêm Bảng điểm chi tiết (Grade Records)
    grades_data = [
        (all_class_ids[0], all_student_ids[0], 9.5, 8.0, 8.5, 8.55, "PASSED", 1, "Học viên xuất sắc, phát âm chuẩn, hoàn thành mục tiêu."),
        (all_class_ids[0], all_student_ids[1] if len(all_student_ids) > 1 else 1, 8.0, 7.0, 7.5, 7.45, "PASSED", 1, "Tiến bộ nhanh, phản xạ nói tốt."),
        (all_class_ids[0], all_student_ids[2] if len(all_student_ids) > 2 else 1, 9.0, 8.5, 9.0, 8.85, "PASSED", 0, "Chờ duyệt khóa điểm từ học vụ."),
        (all_class_ids[1] if len(all_class_ids) > 1 else 1, all_student_ids[3] if len(all_student_ids) > 3 else 1, 7.0, 5.5, 6.0, 6.05, "PASSED", 0, "Cần cải thiện kỹ năng nghe phần part 3 và 4."),
        (all_class_ids[1] if len(all_class_ids) > 1 else 1, all_student_ids[4] if len(all_student_ids) > 4 else 1, 4.0, 4.0, 3.5, 3.75, "FAILED", 1, "Vắng quá số buổi quy định, thi lại cuối kỳ."),
    ]

    for c_id, s_id, att, mid, fin, tot, res_st, is_conf, note in grades_data:
        cursor.execute("""
            INSERT INTO grade_records (class_id, student_id, attendance_score, midterm_score, final_score, total_score, result_status, is_confirmed, note, created_at, updated_at, is_deleted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (c_id, s_id, att, mid, fin, tot, res_st, is_conf, note, now_str, now_str))

    conn.commit()

    # 12. Thêm Tiến trình lên khóa (Course Progressions)
    cursor.execute("SELECT id FROM courses")
    all_courses = [r[0] for r in cursor.fetchall()]
    
    if len(all_courses) >= 2 and len(all_student_ids) >= 2:
        progressions_data = [
            (all_student_ids[0], all_courses[0], all_courses[1], 1, 1, 2, "Đạt chuẩn 8.55, đủ điều kiện học lên khóa nâng cao tiếp theo."),
            (all_student_ids[1], all_courses[0], all_courses[1], 1, 0, None, "Đang chờ nhân viên học vụ kiểm duyệt chứng chỉ."),
        ]
        for s_id, cur_c, next_c, elig, conf, conf_by, note in progressions_data:
            cursor.execute("""
                INSERT INTO course_progressions (student_id, current_course_id, next_course_id, is_eligible, is_confirmed, confirmed_by, confirmed_at, note, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            """, (s_id, cur_c, next_c, elig, conf, conf_by, now_str if conf_by else None, note, now_str, now_str))

        conn.commit()

    conn.close()
    print("✅ Đã nạp thành công bộ dữ liệu phong phú cho toàn bộ 12 bảng!")

if __name__ == "__main__":
    populate_rich_data()
