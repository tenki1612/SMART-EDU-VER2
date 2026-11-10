import sqlite3
from datetime import datetime, date, timedelta, timezone
import bcrypt

def get_hash(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def update_students_and_staff():
    conn = sqlite3.connect(r"d:\Smart-edu\database\language_center.db")
    cursor = conn.cursor()

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    std_pwd_hash = get_hash("student123")

    print("🚀 Bắt đầu điều chỉnh: chỉ giữ 1 nhân viên học vụ và thêm số lượng lớn học viên...")

    # 1. Xóa bớt nhân viên học vụ staff2, staff3 (chỉ giữ đúng 1 nhân viên học vụ duy nhất là 'staff')
    cursor.execute("DELETE FROM users WHERE username IN ('staff2', 'staff3')")
    print("✅ Đã xóa staff2, staff3 - Chỉ giữ lại đúng 1 Nhân viên học vụ ('staff')!")

    # 2. Danh sách 15 học viên mới đa dạng
    extra_students = [
        ("student_an", "hoangan@student.edu.vn", "Nguyễn Hoàng An", "0934000011", "2005-04-10", "12 Hoàng Diệu, Quận 4, TP.HCM"),
        ("student_binh", "thanhbinh@student.edu.vn", "Trần Thanh Bình", "0934000012", "2006-08-22", "34 Nguyễn Tri Phương, Quận 10, TP.HCM"),
        ("student_chi", "kimchi@student.edu.vn", "Lê Thị Kim Chi", "0934000013", "2007-02-15", "56 Phan Đăng Lưu, Phú Nhuận, TP.HCM"),
        ("student_dat", "thanhdat@student.edu.vn", "Phạm Thành Đạt", "0934000014", "2004-11-30", "78 Trần Hưng Đạo, Quận 5, TP.HCM"),
        ("student_giang", "huonggiang@student.edu.vn", "Võ Hương Giang", "0934000015", "2006-05-18", "90 Quang Trung, Gò Vấp, TP.HCM"),
        ("student_hieu", "trunghieu@student.edu.vn", "Đỗ Trung Hiếu", "0934000016", "2005-09-09", "23 Lý Thường Kiệt, Tân Bình, TP.HCM"),
        ("student_khanh", "quockhanh@student.edu.vn", "Bùi Quốc Khánh", "0934000017", "2006-12-01", "45 Nguyễn Thị Minh Khai, Quận 1, TP.HCM"),
        ("student_my", "tramy@student.edu.vn", "Hồ Trà My", "0934000018", "2007-07-07", "67 Bà Huyện Thanh Quan, Quận 3, TP.HCM"),
        ("student_nguyen", "khoinguyen@student.edu.vn", "Dương Khôi Nguyên", "0934000019", "2005-01-20", "89 Võ Văn Ngân, TP. Thủ Đức"),
        ("student_phuc", "hongphuc@student.edu.vn", "Lý Hồng Phúc", "0934000020", "2004-10-14", "101 Hùng Vương, Quận 5, TP.HCM"),
        ("student_quynh", "nhuquynh@student.edu.vn", "Ngô Như Quỳnh", "0934000021", "2006-03-25", "112 Cộng Hòa, Tân Bình, TP.HCM"),
        ("student_son", "thaison@student.edu.vn", "Tô Thái Sơn", "0934000022", "2005-06-19", "134 Xô Viết Nghệ Tĩnh, Bình Thạnh, TP.HCM"),
        ("student_thao", "phuongthao@student.edu.vn", "Mai Phương Thảo", "0934000023", "2007-09-12", "156 Ba Tháng Hai, Quận 10, TP.HCM"),
        ("student_tri", "minhtri@student.edu.vn", "Trịnh Minh Trí", "0934000024", "2006-04-05", "178 Nam Kỳ Khởi Nghĩa, Quận 3, TP.HCM"),
        ("student_vy", "tuongvy@student.edu.vn", "Đặng Tường Vy", "0934000025", "2005-12-28", "190 Nguyễn Trãi, Quận 1, TP.HCM"),
    ]

    code_counter = 8
    for uname, email, full_name, phone, dob, addr in extra_students:
        cursor.execute("SELECT id FROM users WHERE username = ?", (uname,))
        row = cursor.fetchone()
        if not row:
            cursor.execute("""
                INSERT INTO users (username, email, full_name, hashed_password, role, phone, is_active, failed_login_attempts, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, 'STUDENT', ?, 1, 0, ?, ?, 0)
            """, (uname, email, full_name, std_pwd_hash, phone, now_str, now_str))
            uid = cursor.lastrowid
        else:
            uid = row[0]

        std_code = f"HV2026-{code_counter:03d}"
        code_counter += 1

        cursor.execute("SELECT id FROM students WHERE user_id = ?", (uid,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO students (user_id, student_code, date_of_birth, address, status, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, 'ACTIVE', ?, ?, 0)
            """, (uid, std_code, dob, addr, now_str, now_str))

    conn.commit()

    # 3. Phân bổ thêm học viên mới vào các lớp học (class_students) & Tạo đơn đăng ký
    cursor.execute("SELECT id FROM students")
    all_students = [r[0] for r in cursor.fetchall()]
    cursor.execute("SELECT id FROM classes")
    all_classes = [r[0] for r in cursor.fetchall()]

    for i, s_id in enumerate(all_students):
        # Mỗi học viên cho đăng ký 1-2 lớp
        c_id = all_classes[i % len(all_classes)]
        cursor.execute("SELECT id FROM class_students WHERE class_id = ? AND student_id = ?", (c_id, s_id))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO class_students (class_id, student_id, enrolled_at, status, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, 'ENROLLED', ?, ?, 0)
            """, (c_id, s_id, now_str, now_str, now_str))

        # Cập nhật sĩ số hiện tại của lớp
        cursor.execute("SELECT COUNT(*) FROM class_students WHERE class_id = ? AND status = 'ENROLLED'", (c_id,))
        count = cursor.fetchone()[0]
        cursor.execute("UPDATE classes SET current_enrolled = ? WHERE id = ?", (count, c_id))

    conn.commit()

    # 4. Thêm điểm số phong phú cho các học viên mới
    grades_to_add = [
        (all_classes[0], all_students[-1], 9.0, 8.5, 9.0, 8.85, "PASSED", 1, "Học viên xuất sắc, năng nổ trong giờ học."),
        (all_classes[1] if len(all_classes) > 1 else 1, all_students[-2], 8.0, 7.5, 8.0, 7.85, "PASSED", 1, "Kỹ năng nghe tiến bộ vượt bậc."),
        (all_classes[2] if len(all_classes) > 2 else 1, all_students[-3], 6.5, 6.0, 7.0, 6.60, "PASSED", 0, "Cần cải thiện ngữ pháp viết đoạn văn."),
        (all_classes[0], all_students[-4], 4.5, 4.0, 3.5, 3.85, "FAILED", 1, "Thiếu bài tập về nhà và vắng kiểm tra giữa kỳ."),
        (all_classes[1] if len(all_classes) > 1 else 1, all_students[-5], 10.0, 9.5, 9.5, 9.60, "PASSED", 1, "Đạt thủ khoa điểm số của khóa học."),
        (all_classes[2] if len(all_classes) > 2 else 1, all_students[-6], 7.5, 7.0, 7.5, 7.35, "PASSED", 0, "Tiến độ học tập ổn định."),
    ]

    for c_id, s_id, att, mid, fin, tot, res_st, is_conf, note in grades_to_add:
        cursor.execute("SELECT id FROM grade_records WHERE class_id = ? AND student_id = ?", (c_id, s_id))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO grade_records (class_id, student_id, attendance_score, midterm_score, final_score, total_score, result_status, is_confirmed, note, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            """, (c_id, s_id, att, mid, fin, tot, res_st, is_conf, note, now_str, now_str))

    conn.commit()
    conn.close()
    print("✅ Hoàn tất! Đã có 1 nhân viên học vụ duy nhất ('staff') và hơn 25+ học viên sinh động!")

if __name__ == "__main__":
    update_students_and_staff()
