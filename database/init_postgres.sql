-- ============================================================================
-- SMART-EDU LMS - PostgreSQL 16 Initial Database Schema & Seed Data
-- Auto-generated for Language Center Management System
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS unaccent;

DROP TABLE IF EXISTS "users" CASCADE;
CREATE TABLE "users" (
    "username" VARCHAR(50) NOT NULL,
    "email" VARCHAR(100) NOT NULL,
    "full_name" VARCHAR(100) NOT NULL,
    "hashed_password" VARCHAR(255) NOT NULL,
    "role" VARCHAR(14) NOT NULL,
    "phone" VARCHAR(20),
    "avatar_url" VARCHAR(500),
    "is_active" BOOLEAN,
    "failed_login_attempts" INTEGER NOT NULL,
    "locked_until" TIMESTAMP,
    "reset_token" VARCHAR(100),
    "reset_token_expires_at" TIMESTAMP,
    "id" SERIAL PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "is_deleted" BOOLEAN
);

DROP TABLE IF EXISTS "courses" CASCADE;
CREATE TABLE "courses" (
    "code" VARCHAR(50) NOT NULL,
    "title" VARCHAR(150) NOT NULL,
    "description" TEXT,
    "target_level" VARCHAR(100) NOT NULL,
    "duration_weeks" INTEGER,
    "fee" DOUBLE PRECISION,
    "is_active" BOOLEAN,
    "id" SERIAL PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "is_deleted" BOOLEAN
);

DROP TABLE IF EXISTS "classrooms" CASCADE;
CREATE TABLE "classrooms" (
    "room_code" VARCHAR(50) NOT NULL,
    "building" VARCHAR(50),
    "capacity" INTEGER,
    "status" VARCHAR(50),
    "id" SERIAL PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "is_deleted" BOOLEAN
);

DROP TABLE IF EXISTS "students" CASCADE;
CREATE TABLE "students" (
    "user_id" INTEGER NOT NULL,
    "student_code" VARCHAR(50) NOT NULL,
    "date_of_birth" DATE,
    "address" VARCHAR(255),
    "status" VARCHAR(50),
    "id" SERIAL PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "is_deleted" BOOLEAN
);

DROP TABLE IF EXISTS "teachers" CASCADE;
CREATE TABLE "teachers" (
    "user_id" INTEGER NOT NULL,
    "teacher_code" VARCHAR(50) NOT NULL,
    "specialty" VARCHAR(100),
    "degree" VARCHAR(100),
    "status" VARCHAR(50),
    "id" SERIAL PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "is_deleted" BOOLEAN
);

DROP TABLE IF EXISTS "classes" CASCADE;
CREATE TABLE "classes" (
    "class_code" VARCHAR(50) NOT NULL,
    "course_id" INTEGER NOT NULL,
    "teacher_id" INTEGER,
    "max_capacity" INTEGER,
    "current_enrolled" INTEGER,
    "start_date" DATE,
    "end_date" DATE,
    "status" VARCHAR(50),
    "id" SERIAL PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "is_deleted" BOOLEAN
);

DROP TABLE IF EXISTS "course_progressions" CASCADE;
CREATE TABLE "course_progressions" (
    "student_id" INTEGER NOT NULL,
    "current_course_id" INTEGER NOT NULL,
    "next_course_id" INTEGER NOT NULL,
    "is_eligible" BOOLEAN,
    "is_confirmed" BOOLEAN,
    "confirmed_by" INTEGER,
    "confirmed_at" TIMESTAMP,
    "note" TEXT,
    "id" SERIAL PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "is_deleted" BOOLEAN
);

DROP TABLE IF EXISTS "parent_students" CASCADE;
CREATE TABLE "parent_students" (
    "parent_user_id" INTEGER NOT NULL,
    "student_id" INTEGER NOT NULL,
    "relationship_type" VARCHAR(50),
    "id" SERIAL PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "is_deleted" BOOLEAN
);

DROP TABLE IF EXISTS "class_students" CASCADE;
CREATE TABLE "class_students" (
    "class_id" INTEGER NOT NULL,
    "student_id" INTEGER NOT NULL,
    "enrolled_at" TIMESTAMP,
    "status" VARCHAR(50),
    "id" SERIAL PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "is_deleted" BOOLEAN
);

DROP TABLE IF EXISTS "enrollment_requests" CASCADE;
CREATE TABLE "enrollment_requests" (
    "student_id" INTEGER NOT NULL,
    "class_id" INTEGER NOT NULL,
    "request_date" TIMESTAMP,
    "status" VARCHAR(50),
    "note" TEXT,
    "rejection_reason" TEXT,
    "reviewed_by" INTEGER,
    "reviewed_at" TIMESTAMP,
    "id" SERIAL PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "is_deleted" BOOLEAN
);

DROP TABLE IF EXISTS "schedule_sessions" CASCADE;
CREATE TABLE "schedule_sessions" (
    "class_id" INTEGER NOT NULL,
    "classroom_id" INTEGER NOT NULL,
    "teacher_id" INTEGER NOT NULL,
    "session_date" DATE NOT NULL,
    "start_time" VARCHAR(10) NOT NULL,
    "end_time" VARCHAR(10) NOT NULL,
    "slot_name" VARCHAR(50),
    "is_confirmed" BOOLEAN,
    "status" VARCHAR(50),
    "id" SERIAL PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "is_deleted" BOOLEAN
);

DROP TABLE IF EXISTS "grade_records" CASCADE;
CREATE TABLE "grade_records" (
    "class_id" INTEGER NOT NULL,
    "student_id" INTEGER NOT NULL,
    "attendance_score" DOUBLE PRECISION,
    "midterm_score" DOUBLE PRECISION,
    "final_score" DOUBLE PRECISION,
    "total_score" DOUBLE PRECISION,
    "result_status" VARCHAR(50),
    "is_confirmed" BOOLEAN,
    "note" TEXT,
    "id" SERIAL PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "is_deleted" BOOLEAN
);

-- ----------------------------------------------------------------------------
-- DỮ LIỆU KHỞI TẠO (SEED DATA)
-- ----------------------------------------------------------------------------

INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('admin', 'admin_updated@center.edu.vn', 'Nguyễn Văn Quản Trị Cập Nhật', '$2b$12$uptKdBvbAqLvhfJRs6EVVecRjt8.9kcQ4PPUxts4zVr4GQvzpN.mO', 'ADMIN', '0999888777', NULL, TRUE, 1, NULL, NULL, NULL, 1, '2026-11-04 06:07:59.473919', '2026-11-10 02:54:08.896978', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('staff', 'staff@center.edu.vn', 'Trần Thị Học Vụ (Staff)', '$2b$12$VFkFfAq9UQcnB.A.yhgK8uknZX0tsV6gSTRHiqN39erLBag8WNVy6', 'ACADEMIC_STAFF', '0912345678', NULL, TRUE, 0, NULL, NULL, NULL, 2, '2026-11-04 06:07:59.473937', '2026-11-04 06:07:59.473938', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('teacher', 'teacher@center.edu.vn', 'ThS. Lê Hoàng Nam (Teacher)', '$2b$12$a4JkG7ouqNFoV5QQvd46CeURJEHhaQXuks9Mh9ghVpjnxIB2NLxUu', 'TEACHER', '0923456789', NULL, TRUE, 0, NULL, NULL, NULL, 3, '2026-11-04 06:07:59.473939', '2026-11-10 02:54:10.436159', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student', 'student@center.edu.vn', 'Phạm Minh Khang (Student)', '$2b$12$Y9Lrvu9EqOE1NN8QHOkrze/eLHYIc4mlBOvVP.Uz2fo.2jFmAJwsu', 'STUDENT', '0934567890', NULL, TRUE, 0, NULL, NULL, NULL, 4, '2026-11-04 06:07:59.473940', '2026-11-10 02:54:11.619478', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('parent', 'parent@center.edu.vn', 'Phạm Quốc Hùng (Parent)', '$2b$12$YiwnwA3fnVHuMRyvcFi1x.a81tzrGkivs3HiY1M882r9vysvDhCh6', 'PARENT', '0945678901', NULL, TRUE, 0, NULL, NULL, NULL, 5, '2026-11-04 06:07:59.473942', '2026-11-04 06:07:59.473942', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('user_manage_1793773027', 'user_manage_1793773027@center.edu.vn', 'Nguyễn Quản Trị Mục Tiêu', '$2b$12$odXkRgDysTTB7MmP5LbAeede/R8DeezQHwlwjhyVqBStat2sGzOQq', 'TEACHER', '0988776655', NULL, FALSE, 0, NULL, NULL, NULL, 7, '2026-11-04 06:17:07.946353', '2026-11-04 06:17:08.577026', TRUE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('new_student_1793773028', 'new_student_1793773028@student.edu.vn', 'Học Viên Mới Đăng Ký', '$2b$12$ZaD87crhs7PN7xe0j3hLY.4EYhKmIDAPE82ew3ZlfQOuVf4vSUwRC', 'STUDENT', '0987654321', NULL, TRUE, 0, NULL, NULL, NULL, 8, '2026-11-04 06:17:08.868684', '2026-11-04 06:17:08.868689', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('user_manage_1793773677', 'user_manage_1793773677@center.edu.vn', 'Nguyễn Quản Trị Mục Tiêu', '$2b$12$g0bgvDNl57tIcIf9fsZBneaKKzuNLwzOMHF.wgKx/8vR/KoA3lVl2', 'TEACHER', '0988776655', NULL, FALSE, 0, NULL, NULL, NULL, 10, '2026-11-04 06:27:57.843642', '2026-11-04 06:27:58.398273', TRUE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('new_student_1793773678', 'new_student_1793773678@student.edu.vn', 'Học Viên Mới Đăng Ký', '$2b$12$p99mXhxfvQFwN9Sj1GIq6OErSUnL30FIRJHkmWLbuOUhJIpitRMnu', 'STUDENT', '0987654321', NULL, TRUE, 0, NULL, NULL, NULL, 11, '2026-11-04 06:27:58.639058', '2026-11-04 06:27:58.639061', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('teacher_david', 'david.smith@center.edu.vn', 'David Smith (IELTS Native)', '$2b$12$xvNBze3USVoZZXIjFJHozeCI4Cey3BXDaS/EzbVUQU6dmOXrkNPgG', 'TEACHER', '0923000003', NULL, TRUE, 0, NULL, NULL, NULL, 14, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('teacher_lan', 'ngoclan@center.edu.vn', 'Võ Thị Ngọc Lan (TOEFL & Giao Tiếp)', '$2b$12$xvNBze3USVoZZXIjFJHozeCI4Cey3BXDaS/EzbVUQU6dmOXrkNPgG', 'TEACHER', '0923000004', NULL, TRUE, 0, NULL, NULL, NULL, 15, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('teacher_tuan', 'anhtuan@center.edu.vn', 'Đặng Anh Tuấn (TOEIC Master 990)', '$2b$12$xvNBze3USVoZZXIjFJHozeCI4Cey3BXDaS/EzbVUQU6dmOXrkNPgG', 'TEACHER', '0923000005', NULL, TRUE, 0, NULL, NULL, NULL, 16, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_linh', 'ngoclinh@student.edu.vn', 'Hoàng Ngọc Linh', '$2b$12$qwR5aY7nGjSFq62u9L2BVeAYOY1fA92XM1EcyTu6abFClLUbMgy82', 'STUDENT', '0934000002', NULL, TRUE, 0, NULL, NULL, NULL, 17, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_huy', 'quochuy@student.edu.vn', 'Trương Quốc Huy', '$2b$12$qwR5aY7nGjSFq62u9L2BVeAYOY1fA92XM1EcyTu6abFClLUbMgy82', 'STUDENT', '0934000003', NULL, TRUE, 0, NULL, NULL, NULL, 18, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_mai', 'thanhmai@student.edu.vn', 'Đỗ Thanh Mai', '$2b$12$qwR5aY7nGjSFq62u9L2BVeAYOY1fA92XM1EcyTu6abFClLUbMgy82', 'STUDENT', '0934000004', NULL, TRUE, 0, NULL, NULL, NULL, 19, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_bao', 'giabao@student.edu.vn', 'Trần Gia Bảo', '$2b$12$qwR5aY7nGjSFq62u9L2BVeAYOY1fA92XM1EcyTu6abFClLUbMgy82', 'STUDENT', '0934000005', NULL, TRUE, 0, NULL, NULL, NULL, 20, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_yen', 'haiyen@student.edu.vn', 'Phan Hải Yến', '$2b$12$qwR5aY7nGjSFq62u9L2BVeAYOY1fA92XM1EcyTu6abFClLUbMgy82', 'STUDENT', '0934000006', NULL, TRUE, 0, NULL, NULL, NULL, 21, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_nam', 'nhatnam@student.edu.vn', 'Lý Nhật Nam', '$2b$12$qwR5aY7nGjSFq62u9L2BVeAYOY1fA92XM1EcyTu6abFClLUbMgy82', 'STUDENT', '0934000007', NULL, TRUE, 0, NULL, NULL, NULL, 22, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('parent_dung', 'dung.hoang@parent.edu.vn', 'Hoàng Văn Dũng (Bố Ngọc Linh)', '$2b$12$3iwBH7kMmslpBh7wV7JrWOZead44iwRGb7rUX5qAyv3T1xsq58Gpq', 'PARENT', '0945000002', NULL, TRUE, 0, NULL, NULL, NULL, 23, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('parent_huong', 'huong.truong@parent.edu.vn', 'Nguyễn Thu Hương (Mẹ Quốc Huy)', '$2b$12$3iwBH7kMmslpBh7wV7JrWOZead44iwRGb7rUX5qAyv3T1xsq58Gpq', 'PARENT', '0945000003', NULL, TRUE, 0, NULL, NULL, NULL, 24, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('parent_long', 'long.do@parent.edu.vn', 'Đỗ Đình Long (Bố Thanh Mai)', '$2b$12$3iwBH7kMmslpBh7wV7JrWOZead44iwRGb7rUX5qAyv3T1xsq58Gpq', 'PARENT', '0945000004', NULL, TRUE, 0, NULL, NULL, NULL, 25, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_an', 'hoangan@student.edu.vn', 'Nguyễn Hoàng An', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000011', NULL, TRUE, 0, NULL, NULL, NULL, 26, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_binh', 'thanhbinh@student.edu.vn', 'Trần Thanh Bình', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000012', NULL, TRUE, 0, NULL, NULL, NULL, 27, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_chi', 'kimchi@student.edu.vn', 'Lê Thị Kim Chi', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000013', NULL, TRUE, 0, NULL, NULL, NULL, 28, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_dat', 'thanhdat@student.edu.vn', 'Phạm Thành Đạt', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000014', NULL, TRUE, 0, NULL, NULL, NULL, 29, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_giang', 'huonggiang@student.edu.vn', 'Võ Hương Giang', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000015', NULL, TRUE, 0, NULL, NULL, NULL, 30, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_hieu', 'trunghieu@student.edu.vn', 'Đỗ Trung Hiếu', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000016', NULL, TRUE, 0, NULL, NULL, NULL, 31, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_khanh', 'quockhanh@student.edu.vn', 'Bùi Quốc Khánh', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000017', NULL, TRUE, 0, NULL, NULL, NULL, 32, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_my', 'tramy@student.edu.vn', 'Hồ Trà My', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000018', NULL, TRUE, 0, NULL, NULL, NULL, 33, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_nguyen', 'khoinguyen@student.edu.vn', 'Dương Khôi Nguyên', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000019', NULL, TRUE, 0, NULL, NULL, NULL, 34, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_phuc', 'hongphuc@student.edu.vn', 'Lý Hồng Phúc', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000020', NULL, TRUE, 0, NULL, NULL, NULL, 35, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_quynh', 'nhuquynh@student.edu.vn', 'Ngô Như Quỳnh', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000021', NULL, TRUE, 0, NULL, NULL, NULL, 36, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_son', 'thaison@student.edu.vn', 'Tô Thái Sơn', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000022', NULL, TRUE, 0, NULL, NULL, NULL, 37, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_thao', 'phuongthao@student.edu.vn', 'Mai Phương Thảo', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000023', NULL, TRUE, 0, NULL, NULL, NULL, 38, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_tri', 'minhtri@student.edu.vn', 'Trịnh Minh Trí', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000024', NULL, TRUE, 0, NULL, NULL, NULL, 39, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('student_vy', 'tuongvy@student.edu.vn', 'Đặng Tường Vy', '$2b$12$qYHCLDop2d3p6RITsy649uJEOWEqwNNzD4xZX.CBkfBfVtbLjovjm', 'STUDENT', '0934000025', NULL, TRUE, 0, NULL, NULL, NULL, 40, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "users" ("username", "email", "full_name", "hashed_password", "role", "phone", "avatar_url", "is_active", "failed_login_attempts", "locked_until", "reset_token", "reset_token_expires_at", "id", "created_at", "updated_at", "is_deleted") VALUES ('teacher2', 'teacher2@center.edu.vn', 'Cô Trần Thị Mai (Teacher)', '$2b$12$sV0XqGT6arMxfuPHMPFUmOGEZ.hfXsih4mtYdzMmG4ch36yH4.WFC', 'TEACHER', '0923456788', NULL, TRUE, 0, NULL, NULL, NULL, 41, '2026-11-10 04:13:56', '2026-11-10 04:13:56', FALSE);

INSERT INTO "courses" ("code", "title", "description", "target_level", "duration_weeks", "fee", "is_active", "id", "created_at", "updated_at", "is_deleted") VALUES ('IELTS-PREP-65', 'Luyện thi IELTS Chuyên Sâu 6.5+', 'Khóa học tập trung rèn luyện 4 kỹ năng chuẩn học thuật với mục tiêu đầu ra IELTS 6.5.', 'IELTS 6.5', 12, 8500000.0, TRUE, 1, '2026-11-04 06:07:59.502467', '2026-11-04 06:07:59.502470', FALSE);
INSERT INTO "courses" ("code", "title", "description", "target_level", "duration_weeks", "fee", "is_active", "id", "created_at", "updated_at", "is_deleted") VALUES ('IELTS-MASTER-75', 'Luyện thi IELTS Master 7.5+', 'Khóa học nâng cao dành cho học viên đã đạt IELTS 6.5 muốn bứt phá lên 7.5+.', 'IELTS 7.5', 12, 10500000.0, TRUE, 2, '2026-11-04 06:07:59.502471', '2026-11-04 06:07:59.502471', FALSE);
INSERT INTO "courses" ("code", "title", "description", "target_level", "duration_weeks", "fee", "is_active", "id", "created_at", "updated_at", "is_deleted") VALUES ('TOEIC-INTENSIVE-750', 'TOEIC Cấp Tốc 750+', 'Chinh phục kỳ thi TOEIC 2 kỹ năng Nghe - Đọc đạt chuẩn đầu ra đại học và đi làm.', 'TOEIC 750', 8, 5200000.0, TRUE, 3, '2026-11-04 06:07:59.502472', '2026-11-04 06:07:59.502472', FALSE);
INSERT INTO "courses" ("code", "title", "description", "target_level", "duration_weeks", "fee", "is_active", "id", "created_at", "updated_at", "is_deleted") VALUES ('IELTS-FOUNDATION', 'IELTS Foundation 4.5 - 5.5', 'Xây dựng nền tảng ngữ pháp, từ vựng học thuật và phát âm chuẩn quốc tế.', 'IELTS 5.0', 10, 6500000.0, TRUE, 4, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "courses" ("code", "title", "description", "target_level", "duration_weeks", "fee", "is_active", "id", "created_at", "updated_at", "is_deleted") VALUES ('TOEIC-450', 'Luyện Thi TOEIC Khởi Động 450+', 'Khóa học dành cho người mất gốc tiếng Anh cần bằng chuẩn đầu ra tốt nghiệp.', 'TOEIC 450', 8, 3800000.0, TRUE, 5, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "courses" ("code", "title", "description", "target_level", "duration_weeks", "fee", "is_active", "id", "created_at", "updated_at", "is_deleted") VALUES ('COMMUNICATION-PRO', 'Tiếng Anh Giao Tiếp Phản Xạ Đi Làm', 'Rèn luyện giao tiếp thương mại, thuyết trình và đàm phán trong môi trường đa quốc gia.', 'B2 CEFR', 12, 5900000.0, TRUE, 6, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "courses" ("code", "title", "description", "target_level", "duration_weeks", "fee", "is_active", "id", "created_at", "updated_at", "is_deleted") VALUES ('BUSINESS-ENGLISH', 'Tiếng Anh Chuyên Ngành Quản Trị & Đàm Phán', 'Chuyên sâu viết email, báo cáo tài chính và thuật ngữ kinh doanh quốc tế.', 'Advanced Business', 8, 7200000.0, TRUE, 7, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "courses" ("code", "title", "description", "target_level", "duration_weeks", "fee", "is_active", "id", "created_at", "updated_at", "is_deleted") VALUES ('VSTEP-B1-B2', 'Luyện Thi Khung Năng Lực VSTEP B1-B2', 'Khóa luyện thi cấp tốc chuẩn Bộ Giáo Dục & Đào Tạo dành cho giáo viên và cao học.', 'VSTEP B2', 6, 4500000.0, TRUE, 8, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);

INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('P.101', 'Tòa nhà A', 30, 'AVAILABLE', 1, '2026-11-04 06:07:59.510666', '2026-11-04 06:07:59.510669', FALSE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('P.102', 'Tòa nhà A', 25, 'AVAILABLE', 2, '2026-11-04 06:07:59.510670', '2026-11-04 06:07:59.510671', FALSE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('LAB.201', 'Tòa nhà B (Phòng máy)', 35, 'AVAILABLE', 3, '2026-11-04 06:07:59.510671', '2026-11-04 06:07:59.510671', FALSE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('P.301', 'Tòa nhà C', 20, 'AVAILABLE', 4, '2026-11-04 06:07:59.510672', '2026-11-04 06:35:52.042757', FALSE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('LAB-1793773025', 'Tòa nhà B', 40, 'AVAILABLE', 5, '2026-11-04 06:17:05.482278', '2026-11-04 06:17:05.509761', TRUE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('LAB-1793773675', 'Tòa nhà B', 40, 'AVAILABLE', 6, '2026-11-04 06:27:55.540923', '2026-11-04 06:27:55.570522', TRUE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('P.201', 'Tòa nhà B', 30, 'AVAILABLE', 7, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('P.202', 'Tòa nhà B', 35, 'AVAILABLE', 8, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('LAB.202', 'Tòa nhà B (Phòng máy)', 40, 'AVAILABLE', 9, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('VIP.501', 'Tòa nhà Hội Nghị', 15, 'AVAILABLE', 10, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "classrooms" ("room_code", "building", "capacity", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('P.402', 'Tòa nhà D', 25, 'MAINTENANCE', 11, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);

INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (4, '26-04001', '2005-05-15', '123 Nguyễn Văn Cừ, Quận 5, TP.HCM', 'ACTIVE', 1, '2026-11-04 06:07:59.493756', '2026-11-04 06:07:59.493759', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (6, 'HV0006', NULL, NULL, 'ACTIVE', 2, '2026-11-04 06:17:05.780662', '2026-11-04 06:17:05.780665', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (7, 'HV0007', NULL, NULL, 'ACTIVE', 3, '2026-11-04 06:17:07.957402', '2026-11-04 06:17:07.957406', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (8, 'HV0008', NULL, NULL, 'ACTIVE', 4, '2026-11-04 06:17:08.881013', '2026-11-04 06:17:08.881020', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (9, 'HV0009', NULL, NULL, 'ACTIVE', 5, '2026-11-04 06:27:55.879992', '2026-11-04 06:27:55.879995', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (10, 'HV0010', NULL, NULL, 'ACTIVE', 6, '2026-11-04 06:27:57.847043', '2026-11-04 06:27:57.847046', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (11, 'HV0011', NULL, NULL, 'ACTIVE', 7, '2026-11-04 06:27:58.650099', '2026-11-04 06:27:58.650103', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (17, 'HV2026-002', '2006-03-20', '45 Lê Lợi, Quận 1, TP.HCM', 'ACTIVE', 8, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (18, 'HV2026-003', '2005-08-12', '78 Hai Bà Trưng, Quận 3, TP.HCM', 'ACTIVE', 9, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (19, 'HV2026-004', '2007-01-25', '12 Điện Biên Phủ, Bình Thạnh, TP.HCM', 'ACTIVE', 10, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (20, 'HV2026-005', '2006-11-05', '89 Nguyễn Oanh, Gò Vấp, TP.HCM', 'ACTIVE', 11, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (21, 'HV2026-006', '2005-09-18', '234 Võ Văn Tần, Quận 3, TP.HCM', 'ACTIVE', 12, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (22, 'HV2026-007', '2004-12-30', '567 Cách Mạng Tháng 8, Quận 10, TP.HCM', 'ACTIVE', 13, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (26, 'HV2026-008', '2005-04-10', '12 Hoàng Diệu, Quận 4, TP.HCM', 'ACTIVE', 14, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (27, 'HV2026-009', '2006-08-22', '34 Nguyễn Tri Phương, Quận 10, TP.HCM', 'ACTIVE', 15, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (28, 'HV2026-010', '2007-02-15', '56 Phan Đăng Lưu, Phú Nhuận, TP.HCM', 'ACTIVE', 16, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (29, 'HV2026-011', '2004-11-30', '78 Trần Hưng Đạo, Quận 5, TP.HCM', 'ACTIVE', 17, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (30, 'HV2026-012', '2006-05-18', '90 Quang Trung, Gò Vấp, TP.HCM', 'ACTIVE', 18, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (31, 'HV2026-013', '2005-09-09', '23 Lý Thường Kiệt, Tân Bình, TP.HCM', 'ACTIVE', 19, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (32, 'HV2026-014', '2006-12-01', '45 Nguyễn Thị Minh Khai, Quận 1, TP.HCM', 'ACTIVE', 20, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (33, 'HV2026-015', '2007-07-07', '67 Bà Huyện Thanh Quan, Quận 3, TP.HCM', 'ACTIVE', 21, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (34, 'HV2026-016', '2005-01-20', '89 Võ Văn Ngân, TP. Thủ Đức', 'ACTIVE', 22, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (35, 'HV2026-017', '2004-10-14', '101 Hùng Vương, Quận 5, TP.HCM', 'ACTIVE', 23, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (36, 'HV2026-018', '2006-03-25', '112 Cộng Hòa, Tân Bình, TP.HCM', 'ACTIVE', 24, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (37, 'HV2026-019', '2005-06-19', '134 Xô Viết Nghệ Tĩnh, Bình Thạnh, TP.HCM', 'ACTIVE', 25, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (38, 'HV2026-020', '2007-09-12', '156 Ba Tháng Hai, Quận 10, TP.HCM', 'ACTIVE', 26, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (39, 'HV2026-021', '2006-04-05', '178 Nam Kỳ Khởi Nghĩa, Quận 3, TP.HCM', 'ACTIVE', 27, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "students" ("user_id", "student_code", "date_of_birth", "address", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (40, 'HV2026-022', '2005-12-28', '190 Nguyễn Trãi, Quận 1, TP.HCM', 'ACTIVE', 28, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);

INSERT INTO "teachers" ("user_id", "teacher_code", "specialty", "degree", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (3, 'GV2026-001', 'IELTS 8.0 & Academic Writing', 'Master of Applied Linguistics', 'ACTIVE', 1, '2026-11-04 06:07:59.494782', '2026-11-04 06:07:59.494785', FALSE);
INSERT INTO "teachers" ("user_id", "teacher_code", "specialty", "degree", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (7, 'GV0007', 'Giảng viên Ngoại ngữ', 'Cử nhân Ngôn ngữ Anh', 'ACTIVE', 2, '2026-11-04 06:17:07.981077', '2026-11-04 06:17:07.981079', FALSE);
INSERT INTO "teachers" ("user_id", "teacher_code", "specialty", "degree", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (10, 'GV0010', 'Giảng viên Ngoại ngữ', 'Cử nhân Ngôn ngữ Anh', 'ACTIVE', 3, '2026-11-04 06:27:57.863599', '2026-11-04 06:27:57.863602', FALSE);
INSERT INTO "teachers" ("user_id", "teacher_code", "specialty", "degree", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (14, 'GV-2026-ENG', 'IELTS Speaking & Academic Writing 8.5', 'Master of Arts in TESOL (Oxford University)', 'ACTIVE', 4, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "teachers" ("user_id", "teacher_code", "specialty", "degree", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (15, 'GV-2026-TOEFL', 'TOEFL iBT & Tiếng Anh Thương Mại (Business English)', 'Bachelor of English Linguistics (VNU)', 'ACTIVE', 5, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "teachers" ("user_id", "teacher_code", "specialty", "degree", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (16, 'GV-2026-TOEIC', 'TOEIC Listening & Reading 990 Full', 'Chứng chỉ Giảng dạy Quốc tế CELTA', 'ACTIVE', 6, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "teachers" ("user_id", "teacher_code", "specialty", "degree", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (41, 'GV2026-002', 'TOEIC 900 & Giao tiếp phản xạ', 'Bachelor of English Pedagogy', 'ACTIVE', 7, '2026-11-10 04:13:56', '2026-11-10 04:13:56', FALSE);

INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('IELTS-65-K26A', 1, 1, 20, 3, '2026-11-01', '2027-01-24', 'OPEN_FOR_ENROLLMENT', 1, '2026-11-04 06:07:59.521892', '2026-11-04 06:07:59.521896', FALSE);
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('IELTS-75-K26A', 2, 1, 20, 4, '2026-11-20', '2027-02-20', 'OPEN_FOR_ENROLLMENT', 2, '2026-11-04 06:07:59.521897', '2026-11-04 06:27:54.921567', FALSE);
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('TOEIC-750-K12', 3, 1, 25, 3, '2026-11-15', '2027-01-15', 'OPEN_FOR_ENROLLMENT', 3, '2026-11-04 06:07:59.521898', '2026-11-04 06:07:59.521898', FALSE);
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('TEST-CAN-1793773025', 1, NULL, 20, 3, NULL, NULL, 'OPEN_FOR_ENROLLMENT', 4, '2026-11-04 06:17:05.147261', '2026-11-04 06:17:05.427300', TRUE);
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('TEST-CAN-1793773675', 1, NULL, 20, 3, NULL, NULL, 'OPEN_FOR_ENROLLMENT', 5, '2026-11-04 06:27:55.175497', '2026-11-04 06:27:55.476604', TRUE);
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('IELTS-FOUND-K01', 4, 1, 20, 3, '2026-11-15', '2027-01-25', 'OPEN_FOR_ENROLLMENT', 6, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('TOEIC-450-K05', 5, 2, 25, 3, '2026-11-20', '2027-01-20', 'OPEN_FOR_ENROLLMENT', 7, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('COMM-PRO-K02', 6, 3, 15, 3, '2026-12-01', '2027-02-28', 'OPEN_FOR_ENROLLMENT', 8, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('BIZ-ENG-K01', 7, 1, 15, 2, '2026-12-10', '2027-02-10', 'OPEN_FOR_ENROLLMENT', 9, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "classes" ("class_code", "course_id", "teacher_id", "max_capacity", "current_enrolled", "start_date", "end_date", "status", "id", "created_at", "updated_at", "is_deleted") VALUES ('VSTEP-B2-K03', 8, 2, 30, 2, '2026-11-05', '2026-12-20', 'IN_PROGRESS', 10, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);

INSERT INTO "course_progressions" ("student_id", "current_course_id", "next_course_id", "is_eligible", "is_confirmed", "confirmed_by", "confirmed_at", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, 2, TRUE, TRUE, 2, '2026-11-04 06:07:59.535061', 'Học viên đã đạt 8.1 ở khóa IELTS 6.5, đủ điều kiện học lên lớp IELTS Master 7.5+.', 1, '2026-11-04 06:07:59.538541', '2026-11-04 06:07:59.538543', FALSE);
INSERT INTO "course_progressions" ("student_id", "current_course_id", "next_course_id", "is_eligible", "is_confirmed", "confirmed_by", "confirmed_at", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, 2, TRUE, TRUE, 2, '2026-11-10 04:07:15', 'Đạt chuẩn 8.55, đủ điều kiện học lên khóa nâng cao tiếp theo.', 2, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "course_progressions" ("student_id", "current_course_id", "next_course_id", "is_eligible", "is_confirmed", "confirmed_by", "confirmed_at", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 1, 2, TRUE, FALSE, NULL, NULL, 'Đang chờ nhân viên học vụ kiểm duyệt chứng chỉ.', 3, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);

INSERT INTO "parent_students" ("parent_user_id", "student_id", "relationship_type", "id", "created_at", "updated_at", "is_deleted") VALUES (5, 1, 'Bố ruột', 1, '2026-11-04 06:07:59.503734', '2026-11-04 06:07:59.503737', FALSE);
INSERT INTO "parent_students" ("parent_user_id", "student_id", "relationship_type", "id", "created_at", "updated_at", "is_deleted") VALUES (23, 8, 'Bố ruột', 2, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "parent_students" ("parent_user_id", "student_id", "relationship_type", "id", "created_at", "updated_at", "is_deleted") VALUES (24, 9, 'Mẹ ruột', 3, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "parent_students" ("parent_user_id", "student_id", "relationship_type", "id", "created_at", "updated_at", "is_deleted") VALUES (25, 10, 'Bố ruột', 4, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);

INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, '2026-11-04 06:07:59.535936', 'ENROLLED', 1, '2026-11-04 06:07:59.535939', '2026-11-04 06:07:59.535940', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 1, '2026-11-04 06:17:04.884650', 'ENROLLED', 2, '2026-11-04 06:17:04.884654', '2026-11-04 06:27:54.922234', TRUE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 2, '2026-11-10 04:07:15', 'ENROLLED', 3, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (3, 3, '2026-11-10 04:07:15', 'ENROLLED', 4, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (4, 4, '2026-11-10 04:07:15', 'ENROLLED', 5, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (5, 5, '2026-11-10 04:07:15', 'ENROLLED', 6, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (6, 6, '2026-11-10 04:07:15', 'ENROLLED', 7, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (7, 7, '2026-11-10 04:07:15', 'ENROLLED', 8, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (8, 8, '2026-11-10 04:07:15', 'ENROLLED', 9, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (9, 9, '2026-11-10 04:07:15', 'ENROLLED', 10, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (10, 10, '2026-11-10 04:07:15', 'ENROLLED', 11, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 11, '2026-11-10 04:07:15', 'ENROLLED', 12, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 12, '2026-11-10 04:07:15', 'ENROLLED', 13, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (3, 13, '2026-11-10 04:07:15', 'ENROLLED', 14, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (4, 14, '2026-11-10 04:11:18', 'ENROLLED', 15, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (5, 15, '2026-11-10 04:11:18', 'ENROLLED', 16, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (6, 16, '2026-11-10 04:11:18', 'ENROLLED', 17, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (7, 17, '2026-11-10 04:11:18', 'ENROLLED', 18, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (8, 18, '2026-11-10 04:11:18', 'ENROLLED', 19, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (9, 19, '2026-11-10 04:11:18', 'ENROLLED', 20, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (10, 20, '2026-11-10 04:11:18', 'ENROLLED', 21, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 21, '2026-11-10 04:11:18', 'ENROLLED', 22, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 22, '2026-11-10 04:11:18', 'ENROLLED', 23, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (3, 23, '2026-11-10 04:11:18', 'ENROLLED', 24, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (4, 24, '2026-11-10 04:11:18', 'ENROLLED', 25, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (5, 25, '2026-11-10 04:11:18', 'ENROLLED', 26, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (6, 26, '2026-11-10 04:11:18', 'ENROLLED', 27, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (7, 27, '2026-11-10 04:11:18', 'ENROLLED', 28, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "class_students" ("class_id", "student_id", "enrolled_at", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (8, 28, '2026-11-10 04:11:18', 'ENROLLED', 29, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);

INSERT INTO "enrollment_requests" ("student_id", "class_id", "request_date", "status", "note", "rejection_reason", "reviewed_by", "reviewed_at", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, '2026-11-04 06:07:59.537135', 'APPROVED', 'Học viên đã nộp học phí qua chuyển khoản', NULL, 2, '2026-11-04 06:07:59.531679', 1, '2026-11-04 06:07:59.537139', '2026-11-04 06:07:59.537140', FALSE);
INSERT INTO "enrollment_requests" ("student_id", "class_id", "request_date", "status", "note", "rejection_reason", "reviewed_by", "reviewed_at", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 4, '2026-11-04 06:17:05.382888', 'CANCELLED', 'Kiểm thử đăng ký và hủy đơn khi PENDING', NULL, NULL, NULL, 2, '2026-11-04 06:17:05.382891', '2026-11-04 06:17:05.410373', FALSE);
INSERT INTO "enrollment_requests" ("student_id", "class_id", "request_date", "status", "note", "rejection_reason", "reviewed_by", "reviewed_at", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 5, '2026-11-04 06:27:55.439531', 'CANCELLED', 'Kiểm thử đăng ký và hủy đơn khi PENDING', NULL, NULL, NULL, 3, '2026-11-04 06:27:55.439535', '2026-11-04 06:27:55.457364', FALSE);
INSERT INTO "enrollment_requests" ("student_id", "class_id", "request_date", "status", "note", "rejection_reason", "reviewed_by", "reviewed_at", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, '2026-11-10 04:07:15', 'APPROVED', 'Đã thanh toán học phí qua VNPAY', NULL, 2, '2026-11-10 04:07:15', 4, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "enrollment_requests" ("student_id", "class_id", "request_date", "status", "note", "rejection_reason", "reviewed_by", "reviewed_at", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 2, '2026-11-10 04:07:15', 'APPROVED', 'Học viên được duyệt học bổng 20%', NULL, 2, '2026-11-10 04:07:15', 5, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "enrollment_requests" ("student_id", "class_id", "request_date", "status", "note", "rejection_reason", "reviewed_by", "reviewed_at", "id", "created_at", "updated_at", "is_deleted") VALUES (3, 3, '2026-11-10 04:07:15', 'PENDING', 'Chờ kiểm tra đầu vào trực tiếp', NULL, NULL, NULL, 6, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "enrollment_requests" ("student_id", "class_id", "request_date", "status", "note", "rejection_reason", "reviewed_by", "reviewed_at", "id", "created_at", "updated_at", "is_deleted") VALUES (4, 1, '2026-11-10 04:07:15', 'PENDING', 'Đăng ký ca tối thứ 2-4-6', NULL, NULL, NULL, 7, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "enrollment_requests" ("student_id", "class_id", "request_date", "status", "note", "rejection_reason", "reviewed_by", "reviewed_at", "id", "created_at", "updated_at", "is_deleted") VALUES (5, 2, '2026-11-10 04:07:15', 'REJECTED', 'Không đáp ứng điểm sàn đầu vào khóa Master', NULL, 2, '2026-11-10 04:07:15', 8, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);

INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, 1, '2026-11-06', '18:00', '20:00', 'Ca 3 (18:00 - 20:00)', TRUE, 'SCHEDULED', 1, '2026-11-04 06:07:59.539299', '2026-11-04 06:07:59.539300', FALSE);
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, 1, '2026-11-08', '18:00', '20:00', 'Ca 3 (18:00 - 20:00)', TRUE, 'SCHEDULED', 2, '2026-11-04 06:07:59.539301', '2026-11-04 06:07:59.539302', FALSE);
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 2, 2, '2026-11-14', '08:00', '10:00', 'Ca sáng điều chỉnh (08:00 - 10:00)', FALSE, 'SCHEDULED', 3, '2026-11-04 06:17:05.440414', '2026-11-04 06:17:05.470158', TRUE);
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 2, 2, '2026-11-14', '08:00', '10:00', 'Ca sáng điều chỉnh (08:00 - 10:00)', FALSE, 'SCHEDULED', 4, '2026-11-04 06:27:55.490349', '2026-11-04 06:27:55.526093', TRUE);
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, 1, '2026-11-11', '18:00', '20:00', 'Ca 3 (18:00 - 20:00)', TRUE, 'SCHEDULED', 5, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, 1, '2026-11-13', '18:00', '20:00', 'Ca 3 (18:00 - 20:00)', TRUE, 'SCHEDULED', 6, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, 1, '2026-11-15', '18:00', '20:00', 'Ca 3 (18:00 - 20:00)', TRUE, 'SCHEDULED', 7, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 2, 2, '2026-11-12', '08:00', '10:00', 'Ca 1 (08:00 - 10:00)', TRUE, 'SCHEDULED', 8, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 2, 2, '2026-11-14', '08:00', '10:00', 'Ca 1 (08:00 - 10:00)', TRUE, 'SCHEDULED', 9, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (3, 3, 3, '2026-11-12', '14:00', '16:00', 'Ca 2 (14:00 - 16:00)', TRUE, 'SCHEDULED', 10, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "schedule_sessions" ("class_id", "classroom_id", "teacher_id", "session_date", "start_time", "end_time", "slot_name", "is_confirmed", "status", "id", "created_at", "updated_at", "is_deleted") VALUES (3, 3, 3, '2026-11-16', '14:00', '16:00', 'Ca 2 (14:00 - 16:00)', TRUE, 'SCHEDULED', 11, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);

INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, 9.5, 7.5, 8.0, 8.15, 'PASSED', FALSE, 'Học viên tiếp thu tốt, phát âm chuẩn, hoàn thành xuất sắc mục tiêu đầu ra 6.5.', 1, '2026-11-04 06:07:59.537869', '2026-11-04 06:51:32.975748', FALSE);
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 1, 9.5, 8.5, 9.0, 8.95, 'PASSED', FALSE, NULL, 2, '2026-11-04 06:17:04.885280', '2026-11-04 06:27:54.922670', TRUE);
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 1, 9.5, 8.0, 8.5, 8.55, 'PASSED', TRUE, 'Học viên xuất sắc, phát âm chuẩn, hoàn thành mục tiêu.', 3, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 2, 8.0, 7.0, 7.5, 7.45, 'PASSED', TRUE, 'Tiến bộ nhanh, phản xạ nói tốt.', 4, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 3, 9.0, 8.5, 9.0, 8.85, 'PASSED', FALSE, 'Chờ duyệt khóa điểm từ học vụ.', 5, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 4, 7.0, 5.5, 6.0, 6.05, 'PASSED', FALSE, 'Cần cải thiện kỹ năng nghe phần part 3 và 4.', 6, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 5, 4.0, 4.0, 3.5, 3.75, 'FAILED', TRUE, 'Vắng quá số buổi quy định, thi lại cuối kỳ.', 7, '2026-11-10 04:07:15', '2026-11-10 04:07:15', FALSE);
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 28, 9.0, 8.5, 9.0, 8.85, 'PASSED', TRUE, 'Học viên xuất sắc, năng nổ trong giờ học.', 8, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 27, 8.0, 7.5, 8.0, 7.85, 'PASSED', TRUE, 'Kỹ năng nghe tiến bộ vượt bậc.', 9, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (3, 26, 6.5, 6.0, 7.0, 6.6, 'PASSED', FALSE, 'Cần cải thiện ngữ pháp viết đoạn văn.', 10, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (1, 25, 4.5, 4.0, 3.5, 3.85, 'FAILED', TRUE, 'Thiếu bài tập về nhà và vắng kiểm tra giữa kỳ.', 11, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (2, 24, 10.0, 9.5, 9.5, 9.6, 'PASSED', TRUE, 'Đạt thủ khoa điểm số của khóa học.', 12, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);
INSERT INTO "grade_records" ("class_id", "student_id", "attendance_score", "midterm_score", "final_score", "total_score", "result_status", "is_confirmed", "note", "id", "created_at", "updated_at", "is_deleted") VALUES (3, 23, 7.5, 7.0, 7.5, 7.35, 'PASSED', FALSE, 'Tiến độ học tập ổn định.', 13, '2026-11-10 04:11:18', '2026-11-10 04:11:18', FALSE);

-- ----------------------------------------------------------------------------
-- ĐỒNG BỘ SEQUENCES CỦA POSTGRESQL
-- ----------------------------------------------------------------------------

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
