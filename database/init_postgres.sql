-- ============================================================================
-- SMART-EDU LMS - PostgreSQL 16 Initial Database Schema & Seed Data
-- Auto-generated for Language Center Management System
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS unaccent;

-- ------------------------------------------------------------
-- Table: users
-- ------------------------------------------------------------
DROP TABLE IF EXISTS "users" CASCADE;
CREATE TABLE users (
	username VARCHAR(50) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	full_name VARCHAR(100) NOT NULL, 
	hashed_password VARCHAR(255) NOT NULL, 
	role VARCHAR(14) NOT NULL, 
	phone VARCHAR(20), 
	avatar_url VARCHAR(500), 
	is_active BOOLEAN, 
	failed_login_attempts INTEGER NOT NULL, 
	locked_until TIMESTAMP, 
	reset_token VARCHAR(100), 
	reset_token_expires_at TIMESTAMP, 
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	is_deleted BOOLEAN
);

-- ------------------------------------------------------------
-- Table: courses
-- ------------------------------------------------------------
DROP TABLE IF EXISTS "courses" CASCADE;
CREATE TABLE courses (
	code VARCHAR(50) NOT NULL, 
	title VARCHAR(150) NOT NULL, 
	description TEXT, 
	target_level VARCHAR(100) NOT NULL, 
	duration_weeks INTEGER, 
	fee FLOAT, 
	is_active BOOLEAN, 
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	is_deleted BOOLEAN
);

-- ------------------------------------------------------------
-- Table: classrooms
-- ------------------------------------------------------------
DROP TABLE IF EXISTS "classrooms" CASCADE;
CREATE TABLE classrooms (
	room_code VARCHAR(50) NOT NULL, 
	building VARCHAR(50), 
	capacity INTEGER, 
	status VARCHAR(50), 
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	is_deleted BOOLEAN
);

-- ------------------------------------------------------------
-- Table: students
-- ------------------------------------------------------------
DROP TABLE IF EXISTS "students" CASCADE;
CREATE TABLE students (
	user_id SERIAL PRIMARY KEY,
	student_code VARCHAR(50) NOT NULL, 
	date_of_birth DATE, 
	address VARCHAR(255), 
	status VARCHAR(50), 
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	is_deleted BOOLEAN, 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

-- ------------------------------------------------------------
-- Table: teachers
-- ------------------------------------------------------------
DROP TABLE IF EXISTS "teachers" CASCADE;
CREATE TABLE teachers (
	user_id SERIAL PRIMARY KEY,
	teacher_code VARCHAR(50) NOT NULL, 
	specialty VARCHAR(100), 
	degree VARCHAR(100), 
	status VARCHAR(50), 
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	is_deleted BOOLEAN, 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

-- ------------------------------------------------------------
-- Table: classes
-- ------------------------------------------------------------
DROP TABLE IF EXISTS "classes" CASCADE;
CREATE TABLE classes (
	class_code VARCHAR(50) NOT NULL, 
	course_id SERIAL PRIMARY KEY,
	teacher_id INTEGER, 
	max_capacity INTEGER, 
	current_enrolled INTEGER, 
	start_date DATE, 
	end_date DATE, 
	status VARCHAR(50), 
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	is_deleted BOOLEAN, 
	FOREIGN KEY(course_id) REFERENCES courses (id), 
	FOREIGN KEY(teacher_id) REFERENCES teachers (id)
);

-- ------------------------------------------------------------
-- Table: course_progressions
-- ------------------------------------------------------------
DROP TABLE IF EXISTS "course_progressions" CASCADE;
CREATE TABLE course_progressions (
	student_id SERIAL PRIMARY KEY,
	current_course_id SERIAL PRIMARY KEY,
	next_course_id SERIAL PRIMARY KEY,
	is_eligible BOOLEAN, 
	is_confirmed BOOLEAN, 
	confirmed_by INTEGER, 
	confirmed_at TIMESTAMP, 
	note TEXT, 
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	is_deleted BOOLEAN, 
	FOREIGN KEY(student_id) REFERENCES students (id), 
	FOREIGN KEY(current_course_id) REFERENCES courses (id), 
	FOREIGN KEY(next_course_id) REFERENCES courses (id), 
	FOREIGN KEY(confirmed_by) REFERENCES users (id)
);

-- ------------------------------------------------------------
-- Table: parent_students
-- ------------------------------------------------------------
DROP TABLE IF EXISTS "parent_students" CASCADE;
CREATE TABLE parent_students (
	parent_user_id SERIAL PRIMARY KEY,
	student_id SERIAL PRIMARY KEY,
	relationship_type VARCHAR(50), 
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	is_deleted BOOLEAN, 
	FOREIGN KEY(parent_user_id) REFERENCES users (id), 
	FOREIGN KEY(student_id) REFERENCES students (id)
);

-- ------------------------------------------------------------
-- Table: class_students
-- ------------------------------------------------------------
DROP TABLE IF EXISTS "class_students" CASCADE;
CREATE TABLE class_students (
	class_id SERIAL PRIMARY KEY,
	student_id SERIAL PRIMARY KEY,
	enrolled_at TIMESTAMP, 
	status VARCHAR(50), 
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	is_deleted BOOLEAN, 
	FOREIGN KEY(class_id) REFERENCES classes (id), 
	FOREIGN KEY(student_id) REFERENCES students (id)
);

-- ------------------------------------------------------------
-- Table: enrollment_requests
-- ------------------------------------------------------------
DROP TABLE IF EXISTS "enrollment_requests" CASCADE;
CREATE TABLE enrollment_requests (
	student_id SERIAL PRIMARY KEY,
	class_id SERIAL PRIMARY KEY,
	request_date TIMESTAMP, 
	status VARCHAR(50), 
	note TEXT, 
	rejection_reason TEXT, 
	reviewed_by INTEGER, 
	reviewed_at TIMESTAMP, 
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	is_deleted BOOLEAN, 
	FOREIGN KEY(student_id) REFERENCES students (id), 
	FOREIGN KEY(class_id) REFERENCES classes (id), 
	FOREIGN KEY(reviewed_by) REFERENCES users (id)
);

-- ------------------------------------------------------------
-- Table: schedule_sessions
-- ------------------------------------------------------------
DROP TABLE IF EXISTS "schedule_sessions" CASCADE;
CREATE TABLE schedule_sessions (
	class_id SERIAL PRIMARY KEY,
	classroom_id SERIAL PRIMARY KEY,
	teacher_id SERIAL PRIMARY KEY,
	session_date DATE NOT NULL, 
	start_time VARCHAR(10) NOT NULL, 
	end_time VARCHAR(10) NOT NULL, 
	slot_name VARCHAR(50), 
	is_confirmed BOOLEAN, 
	status VARCHAR(50), 
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	is_deleted BOOLEAN, 
	FOREIGN KEY(class_id) REFERENCES classes (id), 
	FOREIGN KEY(classroom_id) REFERENCES classrooms (id), 
	FOREIGN KEY(teacher_id) REFERENCES teachers (id)
);

-- ------------------------------------------------------------
-- Table: grade_records
-- ------------------------------------------------------------
DROP TABLE IF EXISTS "grade_records" CASCADE;
CREATE TABLE grade_records (
	class_id SERIAL PRIMARY KEY,
	student_id SERIAL PRIMARY KEY,
	attendance_score FLOAT, 
	midterm_score FLOAT, 
	final_score FLOAT, 
	total_score FLOAT, 
	result_status VARCHAR(50), 
	is_confirmed BOOLEAN, 
	note TEXT, 
	id SERIAL PRIMARY KEY,
	created_at TIMESTAMP, 
	updated_at TIMESTAMP, 
	is_deleted BOOLEAN, 
	FOREIGN KEY(class_id) REFERENCES classes (id), 
	FOREIGN KEY(student_id) REFERENCES students (id)
);


-- ============================================================
-- SEED DATA
-- ============================================================

-- Data for users (11 rows)
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('admin', 'admin_updated@center.edu.vn', 'Nguyễn Văn Quản Trị Cập Nhật', '$2b$12$uptKdBvbAqLvhfJRs6EVVecRjt8.9kcQ4PPUxts4zVr4GQvzpN.mO', 'ADMIN', '0999888777', NULL, TRUE, 0, NULL, NULL, NULL, 1, '2026-11-04 06:07:59.473919', '2026-11-04 06:27:58.925928', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('staff', 'staff@center.edu.vn', 'Trần Thị Học Vụ (Staff)', '$2b$12$VFkFfAq9UQcnB.A.yhgK8uknZX0tsV6gSTRHiqN39erLBag8WNVy6', 'ACADEMIC_STAFF', '0912345678', NULL, TRUE, 0, NULL, NULL, NULL, 2, '2026-11-04 06:07:59.473937', '2026-11-04 06:07:59.473938', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('teacher', 'teacher@center.edu.vn', 'ThS. Lê Hoàng Nam (Teacher)', '$2b$12$kLUYJZLYqUVZZpkWhnDYS.QWt2mRM4hCPcTmvAC9T8QsgWUmtt3tW', 'TEACHER', '0923456789', NULL, TRUE, 0, NULL, NULL, NULL, 3, '2026-11-04 06:07:59.473939', '2026-11-04 06:07:59.473940', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student', 'student@center.edu.vn', 'Phạm Minh Khang (Student)', '$2b$12$ESnjS/MPYmbDDgCniifvxO9MHHNIjker5Fz2Ir05ds7yrPfJR3fgG', 'STUDENT', '0934567890', NULL, TRUE, 0, NULL, NULL, NULL, 4, '2026-11-04 06:07:59.473940', '2026-11-04 06:07:59.473941', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('parent', 'parent@center.edu.vn', 'Phạm Quốc Hùng (Parent)', '$2b$12$YiwnwA3fnVHuMRyvcFi1x.a81tzrGkivs3HiY1M882r9vysvDhCh6', 'PARENT', '0945678901', NULL, TRUE, 0, NULL, NULL, NULL, 5, '2026-11-04 06:07:59.473942', '2026-11-04 06:07:59.473942', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('locktest_1793773025', 'locktest_1793773025@smartedu.edu.vn', 'Kiểm Thử Khóa Đăng Nhập', '$2b$12$PxZ5lRN7pDnmuAMe3np/zejxizHPXmutKBPEHVOll65VOsoIU0YkS', 'STUDENT', NULL, NULL, TRUE, 0, NULL, NULL, NULL, 6, '2026-11-04 06:17:05.768031', '2026-11-04 06:17:07.428996', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('user_manage_1793773027', 'user_manage_1793773027@center.edu.vn', 'Nguyễn Quản Trị Mục Tiêu', '$2b$12$odXkRgDysTTB7MmP5LbAeede/R8DeezQHwlwjhyVqBStat2sGzOQq', 'TEACHER', '0988776655', NULL, FALSE, 0, NULL, NULL, NULL, 7, '2026-11-04 06:17:07.946353', '2026-11-04 06:17:08.577026', TRUE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('new_student_1793773028', 'new_student_1793773028@student.edu.vn', 'Học Viên Mới Đăng Ký', '$2b$12$ZaD87crhs7PN7xe0j3hLY.4EYhKmIDAPE82ew3ZlfQOuVf4vSUwRC', 'STUDENT', '0987654321', NULL, TRUE, 0, NULL, NULL, NULL, 8, '2026-11-04 06:17:08.868684', '2026-11-04 06:17:08.868689', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('locktest_1793773675', 'locktest_1793773675@smartedu.edu.vn', 'Kiểm Thử Khóa Đăng Nhập', '$2b$12$RJXIzpNBV66urySuMblr0uELLe2SvVrziVS4KHa86bOohwEGdlgAy', 'STUDENT', NULL, NULL, TRUE, 0, NULL, NULL, NULL, 9, '2026-11-04 06:27:55.867935', '2026-11-04 06:27:57.356990', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('user_manage_1793773677', 'user_manage_1793773677@center.edu.vn', 'Nguyễn Quản Trị Mục Tiêu', '$2b$12$g0bgvDNl57tIcIf9fsZBneaKKzuNLwzOMHF.wgKx/8vR/KoA3lVl2', 'TEACHER', '0988776655', NULL, FALSE, 0, NULL, NULL, NULL, 10, '2026-11-04 06:27:57.843642', '2026-11-04 06:27:58.398273', TRUE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('new_student_1793773678', 'new_student_1793773678@student.edu.vn', 'Học Viên Mới Đăng Ký', '$2b$12$p99mXhxfvQFwN9Sj1GIq6OErSUnL30FIRJHkmWLbuOUhJIpitRMnu', 'STUDENT', '0987654321', NULL, TRUE, 0, NULL, NULL, NULL, 11, '2026-11-04 06:27:58.639058', '2026-11-04 06:27:58.639061', FALSE);

-- Data for courses (3 rows)
INSERT INTO "courses" ("code", "title", "description", "target_level", "duration_weeks", "fee", "is_active", "id", "created_at", "updated_at", "is_deleted") VALUES ('IELTS-PREP-65', 'Luyện thi IELTS Chuyên Sâu 6.5+', 'Khóa học tập trung rèn luyện 4 kỹ năng chuẩn học thuật với mục tiêu đầu ra IELTS 6.5.', 'IELTS 6.5', 12, 8500000.0, TRUE, 1, '2026-11-04 06:07:59.502467', '2026-11-04 06:07:59.502470', FALSE);
INSERT INTO "courses" ("code", "title", "description", "target_level", "duration_weeks", "fee", "is_active", "id", "created_at", "updated_at", "is_deleted") VALUES ('IELTS-MASTER-75', 'Luyện thi IELTS Master 7.5+', 'Khóa học nâng cao dành cho học viên đã đạt IELTS 6.5 muốn bứt phá lên 7.5+.', 'IELTS 7.5', 12, 10500000.0, TRUE, 2, '2026-11-04 06:07:59.502471', '2026-11-04 06:07:59.502471', FALSE);
INSERT INTO "courses" ("code", "title", "description", "target_level", "duration_weeks", "fee", "is_active", "id", "created_at", "updated_at", "is_deleted") VALUES ('TOEIC-INTENSIVE-750', 'TOEIC Cấp Tốc 750+', 'Chinh phục kỳ thi TOEIC 2 kỹ năng Nghe - Đọc đạt chuẩn đầu ra đại học và đi làm.', 'TOEIC 750', 8, 5200000.0, TRUE, 3, '2026-11-04 06:07:59.502472', '2026-11-04 06:07:59.502472', FALSE);

-- Data for classrooms (6 rows)
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('P.101', 'Tòa nhà A', 30, 'AVAILABLE', 1, '2026-11-04 06:07:59.510666', '2026-11-04 06:07:59.510669', FALSE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('P.102', 'Tòa nhà A', 25, 'AVAILABLE', 2, '2026-11-04 06:07:59.510670', '2026-11-04 06:07:59.510671', FALSE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('LAB.201', 'Tòa nhà B (Phòng máy)', 35, 'AVAILABLE', 3, '2026-11-04 06:07:59.510671', '2026-11-04 06:07:59.510671', FALSE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('P.301', 'Tòa nhà C', 20, 'AVAILABLE', 4, '2026-11-04 06:07:59.510672', '2026-11-04 06:35:52.042757', FALSE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('LAB-1793773025', 'Tòa nhà B', 40, 'AVAILABLE', 5, '2026-11-04 06:17:05.482278', '2026-11-04 06:17:05.509761', TRUE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('LAB-1793773675', 'Tòa nhà B', 40, 'AVAILABLE', 6, '2026-11-04 06:27:55.540923', '2026-11-04 06:27:55.570522', TRUE);

-- Data for students (7 rows)
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (4, '26-04001', '2005-05-15', '123 Nguyễn Văn Cừ, Quận 5, TP.HCM', 'ACTIVE', 1, '2026-11-04 06:07:59.493756', '2026-11-04 06:07:59.493759', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (6, 'HV0006', NULL, NULL, 'ACTIVE', 2, '2026-11-04 06:17:05.780662', '2026-11-04 06:17:05.780665', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (7, 'HV0007', NULL, NULL, 'ACTIVE', 3, '2026-11-04 06:17:07.957402', '2026-11-04 06:17:07.957406', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (8, 'HV0008', NULL, NULL, 'ACTIVE', 4, '2026-11-04 06:17:08.881013', '2026-11-04 06:17:08.881020', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (9, 'HV0009', NULL, NULL, 'ACTIVE', 5, '2026-11-04 06:27:55.879992', '2026-11-04 06:27:55.879995', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (10, 'HV0010', NULL, NULL, 'ACTIVE', 6, '2026-11-04 06:27:57.847043', '2026-11-04 06:27:57.847046', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (11, 'HV0011', NULL, NULL, 'ACTIVE', 7, '2026-11-04 06:27:58.650099', '2026-11-04 06:27:58.650103', FALSE);

-- Data for teachers (3 rows)
INSERT INTO "teachers" ("user_id", "teacher_code", "specialty", "degree", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (3, 'GV2026-001', 'IELTS 8.0 & Academic Writing', 'Master of Applied Linguistics', 'ACTIVE', 1, '2026-11-04 06:07:59.494782', '2026-11-04 06:07:59.494785', FALSE);
INSERT INTO "teachers" ("user_id", "teacher_code", "specialty", "degree", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (7, 'GV0007', 'Giảng viên Ngoại ngữ', 'Cử nhân Ngôn ngữ Anh', 'ACTIVE', 2, '2026-11-04 06:17:07.981077', '2026-11-04 06:17:07.981079', FALSE);
INSERT INTO "teachers" ("user_id", "teacher_code", "specialty", "degree", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (10, 'GV0010', 'Giảng viên Ngoại ngữ', 'Cử nhân Ngôn ngữ Anh', 'ACTIVE', 3, '2026-11-04 06:27:57.863599', '2026-11-04 06:27:57.863602', FALSE);

-- Data for classes (5 rows)
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('IELTS-65-K26A', 1, 1, 20, 1, '2026-11-01', '2027-01-24', 'OPEN_FOR_ENROLLMENT', 1, '2026-11-04 06:07:59.521892', '2026-11-04 06:07:59.521896', FALSE);
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('IELTS-75-K26A', 2, 1, 20, 0, '2026-11-20', '2027-02-20', 'OPEN_FOR_ENROLLMENT', 2, '2026-11-04 06:07:59.521897', '2026-11-04 06:27:54.921567', FALSE);
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('TOEIC-750-K12', 3, 1, 25, 0, '2026-11-15', '2027-01-15', 'OPEN_FOR_ENROLLMENT', 3, '2026-11-04 06:07:59.521898', '2026-11-04 06:07:59.521898', FALSE);
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('TEST-CAN-1793773025', 1, NULL, 20, 0, NULL, NULL, 'OPEN_FOR_ENROLLMENT', 4, '2026-11-04 06:17:05.147261', '2026-11-04 06:17:05.427300', TRUE);
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('TEST-CAN-1793773675', 1, NULL, 20, 0, NULL, NULL, 'OPEN_FOR_ENROLLMENT', 5, '2026-11-04 06:27:55.175497', '2026-11-04 06:27:55.476604', TRUE);

-- Data for course_progressions (1 rows)
INSERT INTO "course_progressions" ("student_id", "current_course_id", "next_course_id", "is_eligible", "is_confirmed", "confirmed_by", "confirmed_at", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, 2, TRUE, TRUE, 2, '2026-11-04 06:07:59.535061', 'Học viên đã đạt 8.1 ở khóa IELTS 6.5, đủ điều kiện học lên lớp IELTS Master 7.5+.', 1, '2026-11-04 06:07:59.538541', '2026-11-04 06:07:59.538543', FALSE);

-- Data for parent_students (1 rows)
INSERT INTO "parent_students" ("parent_user_id", "student_id", "relationship_type", "id", "created_at", "updated_at", "is_deleted") VALUES (5, 1, 'Bố ruột', 1, '2026-11-04 06:07:59.503734', '2026-11-04 06:07:59.503737', FALSE);

-- Data for class_students (2 rows)
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, '2026-11-04 06:07:59.535936', 'ENROLLED', 1, '2026-11-04 06:07:59.535939', '2026-11-04 06:07:59.535940', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 1, '2026-11-04 06:17:04.884650', 'ENROLLED', 2, '2026-11-04 06:17:04.884654', '2026-11-04 06:27:54.922234', TRUE);

-- Data for enrollment_requests (3 rows)
INSERT INTO "enrollment_requests" ("student_id", "class_id", "request_date", "status", "note", "rejection_reason", "reviewed_by", "reviewed_at", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, '2026-11-04 06:07:59.537135', 'APPROVED', 'Học viên đã nộp học phí qua chuyển khoản', NULL, 2, '2026-11-04 06:07:59.531679', 1, '2026-11-04 06:07:59.537139', '2026-11-04 06:07:59.537140', FALSE);
INSERT INTO "enrollment_requests" ("student_id", "class_id", "request_date", "status", "note", "rejection_reason", "reviewed_by", "reviewed_at", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 4, '2026-11-04 06:17:05.382888', 'CANCELLED', 'Kiểm thử đăng ký và hủy đơn khi PENDING', NULL, NULL, NULL, 2, '2026-11-04 06:17:05.382891', '2026-11-04 06:17:05.410373', FALSE);
INSERT INTO "enrollment_requests" ("student_id", "class_id", "request_date", "status", "note", "rejection_reason", "reviewed_by", "reviewed_at", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 5, '2026-11-04 06:27:55.439531', 'CANCELLED', 'Kiểm thử đăng ký và hủy đơn khi PENDING', NULL, NULL, NULL, 3, '2026-11-04 06:27:55.439535', '2026-11-04 06:27:55.457364', FALSE);

-- Data for schedule_sessions (4 rows)
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, 1, '2026-11-06', '18:00', '20:00', 'Ca 3 (18:00 - 20:00)', TRUE, 'SCHEDULED', 1, '2026-11-04 06:07:59.539299', '2026-11-04 06:07:59.539300', FALSE);
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, 1, '2026-11-08', '18:00', '20:00', 'Ca 3 (18:00 - 20:00)', TRUE, 'SCHEDULED', 2, '2026-11-04 06:07:59.539301', '2026-11-04 06:07:59.539302', FALSE);
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 2, 2, '2026-11-14', '08:00', '10:00', 'Ca sáng điều chỉnh (08:00 - 10:00)', FALSE, 'SCHEDULED', 3, '2026-11-04 06:17:05.440414', '2026-11-04 06:17:05.470158', TRUE);
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 2, 2, '2026-11-14', '08:00', '10:00', 'Ca sáng điều chỉnh (08:00 - 10:00)', FALSE, 'SCHEDULED', 4, '2026-11-04 06:27:55.490349', '2026-11-04 06:27:55.526093', TRUE);

-- Data for grade_records (2 rows)
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, 9.5, 7.5, 8.0, 8.15, 'PASSED', FALSE, 'Học viên tiếp thu tốt, phát âm chuẩn, hoàn thành xuất sắc mục tiêu đầu ra 6.5.', 1, '2026-11-04 06:07:59.537869', '2026-11-04 06:51:32.975748', FALSE);
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 1, 9.5, 8.5, 9.0, 8.95, 'PASSED', FALSE, NULL, 2, '2026-11-04 06:17:04.885280', '2026-11-04 06:27:54.922670', TRUE);


-- ============================================================
-- RESET AUTO-INCREMENT SEQUENCES
-- ============================================================

SELECT setval(pg_get_serial_sequence('"users"', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "users";
SELECT setval(pg_get_serial_sequence('"courses"', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "courses";
SELECT setval(pg_get_serial_sequence('"classrooms"', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "classrooms";
SELECT setval(pg_get_serial_sequence('"students"', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "students";
SELECT setval(pg_get_serial_sequence('"teachers"', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "teachers";
SELECT setval(pg_get_serial_sequence('"classes"', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "classes";
SELECT setval(pg_get_serial_sequence('"course_progressions"', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "course_progressions";
SELECT setval(pg_get_serial_sequence('"parent_students"', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "parent_students";
SELECT setval(pg_get_serial_sequence('"class_students"', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "class_students";
SELECT setval(pg_get_serial_sequence('"enrollment_requests"', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "enrollment_requests";
SELECT setval(pg_get_serial_sequence('"schedule_sessions"', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "schedule_sessions";
SELECT setval(pg_get_serial_sequence('"grade_records"', 'id'), coalesce(max(id), 1), max(id) IS NOT null) FROM "grade_records";