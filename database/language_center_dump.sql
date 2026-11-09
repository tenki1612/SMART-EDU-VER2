BEGIN TRANSACTION;
CREATE TABLE class_students (
	class_id INTEGER NOT NULL, 
	student_id INTEGER NOT NULL, 
	enrolled_at DATETIME, 
	status VARCHAR(50), 
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	is_deleted BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(class_id) REFERENCES classes (id), 
	FOREIGN KEY(student_id) REFERENCES students (id)
);
INSERT INTO "class_students" VALUES(1,1,'2026-11-04 06:07:59.535936','ENROLLED',1,'2026-11-04 06:07:59.535939','2026-11-04 06:07:59.535940',0);
INSERT INTO "class_students" VALUES(2,1,'2026-11-04 06:17:04.884650','ENROLLED',2,'2026-11-04 06:17:04.884654','2026-11-04 06:27:54.922234',1);
CREATE TABLE classes (
	class_code VARCHAR(50) NOT NULL, 
	course_id INTEGER NOT NULL, 
	teacher_id INTEGER, 
	max_capacity INTEGER, 
	current_enrolled INTEGER, 
	start_date DATE, 
	end_date DATE, 
	status VARCHAR(50), 
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	is_deleted BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(course_id) REFERENCES courses (id), 
	FOREIGN KEY(teacher_id) REFERENCES teachers (id)
);
INSERT INTO "classes" VALUES('IELTS-65-K26A',1,1,20,1,'2026-11-01','2027-01-24','OPEN_FOR_ENROLLMENT',1,'2026-11-04 06:07:59.521892','2026-11-04 06:07:59.521896',0);
INSERT INTO "classes" VALUES('IELTS-75-K26A',2,1,20,0,'2026-11-20','2027-02-20','OPEN_FOR_ENROLLMENT',2,'2026-11-04 06:07:59.521897','2026-11-04 06:27:54.921567',0);
INSERT INTO "classes" VALUES('TOEIC-750-K12',3,1,25,0,'2026-11-15','2027-01-15','OPEN_FOR_ENROLLMENT',3,'2026-11-04 06:07:59.521898','2026-11-04 06:07:59.521898',0);
INSERT INTO "classes" VALUES('TEST-CAN-1793773025',1,NULL,20,0,NULL,NULL,'OPEN_FOR_ENROLLMENT',4,'2026-11-04 06:17:05.147261','2026-11-04 06:17:05.427300',1);
INSERT INTO "classes" VALUES('TEST-CAN-1793773675',1,NULL,20,0,NULL,NULL,'OPEN_FOR_ENROLLMENT',5,'2026-11-04 06:27:55.175497','2026-11-04 06:27:55.476604',1);
CREATE TABLE classrooms (
	room_code VARCHAR(50) NOT NULL, 
	building VARCHAR(50), 
	capacity INTEGER, 
	status VARCHAR(50), 
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	is_deleted BOOLEAN, 
	PRIMARY KEY (id)
);
INSERT INTO "classrooms" VALUES('P.101','Tòa nhà A',30,'AVAILABLE',1,'2026-11-04 06:07:59.510666','2026-11-04 06:07:59.510669',0);
INSERT INTO "classrooms" VALUES('P.102','Tòa nhà A',25,'AVAILABLE',2,'2026-11-04 06:07:59.510670','2026-11-04 06:07:59.510671',0);
INSERT INTO "classrooms" VALUES('LAB.201','Tòa nhà B (Phòng máy)',35,'AVAILABLE',3,'2026-11-04 06:07:59.510671','2026-11-04 06:07:59.510671',0);
INSERT INTO "classrooms" VALUES('P.301','Tòa nhà C',20,'AVAILABLE',4,'2026-11-04 06:07:59.510672','2026-11-04 06:35:52.042757',0);
INSERT INTO "classrooms" VALUES('LAB-1793773025','Tòa nhà B',40,'AVAILABLE',5,'2026-11-04 06:17:05.482278','2026-11-04 06:17:05.509761',1);
INSERT INTO "classrooms" VALUES('LAB-1793773675','Tòa nhà B',40,'AVAILABLE',6,'2026-11-04 06:27:55.540923','2026-11-04 06:27:55.570522',1);
CREATE TABLE course_progressions (
	student_id INTEGER NOT NULL, 
	current_course_id INTEGER NOT NULL, 
	next_course_id INTEGER NOT NULL, 
	is_eligible BOOLEAN, 
	is_confirmed BOOLEAN, 
	confirmed_by INTEGER, 
	confirmed_at DATETIME, 
	note TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	is_deleted BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(student_id) REFERENCES students (id), 
	FOREIGN KEY(current_course_id) REFERENCES courses (id), 
	FOREIGN KEY(next_course_id) REFERENCES courses (id), 
	FOREIGN KEY(confirmed_by) REFERENCES users (id)
);
INSERT INTO "course_progressions" VALUES(1,1,2,1,1,2,'2026-11-04 06:07:59.535061','Học viên đã đạt 8.1 ở khóa IELTS 6.5, đủ điều kiện học lên lớp IELTS Master 7.5+.',1,'2026-11-04 06:07:59.538541','2026-11-04 06:07:59.538543',0);
CREATE TABLE courses (
	code VARCHAR(50) NOT NULL, 
	title VARCHAR(150) NOT NULL, 
	description TEXT, 
	target_level VARCHAR(100) NOT NULL, 
	duration_weeks INTEGER, 
	fee FLOAT, 
	is_active BOOLEAN, 
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	is_deleted BOOLEAN, 
	PRIMARY KEY (id)
);
INSERT INTO "courses" VALUES('IELTS-PREP-65','Luyện thi IELTS Chuyên Sâu 6.5+','Khóa học tập trung rèn luyện 4 kỹ năng chuẩn học thuật với mục tiêu đầu ra IELTS 6.5.','IELTS 6.5',12,8500000.0,1,1,'2026-11-04 06:07:59.502467','2026-11-04 06:07:59.502470',0);
INSERT INTO "courses" VALUES('IELTS-MASTER-75','Luyện thi IELTS Master 7.5+','Khóa học nâng cao dành cho học viên đã đạt IELTS 6.5 muốn bứt phá lên 7.5+.','IELTS 7.5',12,10500000.0,1,2,'2026-11-04 06:07:59.502471','2026-11-04 06:07:59.502471',0);
INSERT INTO "courses" VALUES('TOEIC-INTENSIVE-750','TOEIC Cấp Tốc 750+','Chinh phục kỳ thi TOEIC 2 kỹ năng Nghe - Đọc đạt chuẩn đầu ra đại học và đi làm.','TOEIC 750',8,5200000.0,1,3,'2026-11-04 06:07:59.502472','2026-11-04 06:07:59.502472',0);
CREATE TABLE enrollment_requests (
	student_id INTEGER NOT NULL, 
	class_id INTEGER NOT NULL, 
	request_date DATETIME, 
	status VARCHAR(50), 
	note TEXT, 
	rejection_reason TEXT, 
	reviewed_by INTEGER, 
	reviewed_at DATETIME, 
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	is_deleted BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(student_id) REFERENCES students (id), 
	FOREIGN KEY(class_id) REFERENCES classes (id), 
	FOREIGN KEY(reviewed_by) REFERENCES users (id)
);
INSERT INTO "enrollment_requests" VALUES(1,1,'2026-11-04 06:07:59.537135','APPROVED','Học viên đã nộp học phí qua chuyển khoản',NULL,2,'2026-11-04 06:07:59.531679',1,'2026-11-04 06:07:59.537139','2026-11-04 06:07:59.537140',0);
INSERT INTO "enrollment_requests" VALUES(1,4,'2026-11-04 06:17:05.382888','CANCELLED','Kiểm thử đăng ký và hủy đơn khi PENDING',NULL,NULL,NULL,2,'2026-11-04 06:17:05.382891','2026-11-04 06:17:05.410373',0);
INSERT INTO "enrollment_requests" VALUES(1,5,'2026-11-04 06:27:55.439531','CANCELLED','Kiểm thử đăng ký và hủy đơn khi PENDING',NULL,NULL,NULL,3,'2026-11-04 06:27:55.439535','2026-11-04 06:27:55.457364',0);
CREATE TABLE grade_records (
	class_id INTEGER NOT NULL, 
	student_id INTEGER NOT NULL, 
	attendance_score FLOAT, 
	midterm_score FLOAT, 
	final_score FLOAT, 
	total_score FLOAT, 
	result_status VARCHAR(50), 
	is_confirmed BOOLEAN, 
	note TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	is_deleted BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(class_id) REFERENCES classes (id), 
	FOREIGN KEY(student_id) REFERENCES students (id)
);
INSERT INTO "grade_records" VALUES(1,1,9.5,7.5,8.0,8.15,'PASSED',0,'Học viên tiếp thu tốt, phát âm chuẩn, hoàn thành xuất sắc mục tiêu đầu ra 6.5.',1,'2026-11-04 06:07:59.537869','2026-11-04 06:51:32.975748',0);
INSERT INTO "grade_records" VALUES(2,1,9.5,8.5,9.0,8.95,'PASSED',0,NULL,2,'2026-11-04 06:17:04.885280','2026-11-04 06:27:54.922670',1);
CREATE TABLE parent_students (
	parent_user_id INTEGER NOT NULL, 
	student_id INTEGER NOT NULL, 
	relationship_type VARCHAR(50), 
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	is_deleted BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parent_user_id) REFERENCES users (id), 
	FOREIGN KEY(student_id) REFERENCES students (id)
);
INSERT INTO "parent_students" VALUES(5,1,'Bố ruột',1,'2026-11-04 06:07:59.503734','2026-11-04 06:07:59.503737',0);
CREATE TABLE schedule_sessions (
	class_id INTEGER NOT NULL, 
	classroom_id INTEGER NOT NULL, 
	teacher_id INTEGER NOT NULL, 
	session_date DATE NOT NULL, 
	start_time VARCHAR(10) NOT NULL, 
	end_time VARCHAR(10) NOT NULL, 
	slot_name VARCHAR(50), 
	is_confirmed BOOLEAN, 
	status VARCHAR(50), 
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	is_deleted BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(class_id) REFERENCES classes (id), 
	FOREIGN KEY(classroom_id) REFERENCES classrooms (id), 
	FOREIGN KEY(teacher_id) REFERENCES teachers (id)
);
INSERT INTO "schedule_sessions" VALUES(1,1,1,'2026-11-06','18:00','20:00','Ca 3 (18:00 - 20:00)',1,'SCHEDULED',1,'2026-11-04 06:07:59.539299','2026-11-04 06:07:59.539300',0);
INSERT INTO "schedule_sessions" VALUES(1,1,1,'2026-11-08','18:00','20:00','Ca 3 (18:00 - 20:00)',1,'SCHEDULED',2,'2026-11-04 06:07:59.539301','2026-11-04 06:07:59.539302',0);
INSERT INTO "schedule_sessions" VALUES(1,2,2,'2026-11-14','08:00','10:00','Ca sáng điều chỉnh (08:00 - 10:00)',0,'SCHEDULED',3,'2026-11-04 06:17:05.440414','2026-11-04 06:17:05.470158',1);
INSERT INTO "schedule_sessions" VALUES(1,2,2,'2026-11-14','08:00','10:00','Ca sáng điều chỉnh (08:00 - 10:00)',0,'SCHEDULED',4,'2026-11-04 06:27:55.490349','2026-11-04 06:27:55.526093',1);
CREATE TABLE students (
	user_id INTEGER NOT NULL, 
	student_code VARCHAR(50) NOT NULL, 
	date_of_birth DATE, 
	address VARCHAR(255), 
	status VARCHAR(50), 
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	is_deleted BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO "students" VALUES(4,'26-04001','2005-05-15','123 Nguyễn Văn Cừ, Quận 5, TP.HCM','ACTIVE',1,'2026-11-04 06:07:59.493756','2026-11-04 06:07:59.493759',0);
INSERT INTO "students" VALUES(6,'HV0006',NULL,NULL,'ACTIVE',2,'2026-11-04 06:17:05.780662','2026-11-04 06:17:05.780665',0);
INSERT INTO "students" VALUES(7,'HV0007',NULL,NULL,'ACTIVE',3,'2026-11-04 06:17:07.957402','2026-11-04 06:17:07.957406',0);
INSERT INTO "students" VALUES(8,'HV0008',NULL,NULL,'ACTIVE',4,'2026-11-04 06:17:08.881013','2026-11-04 06:17:08.881020',0);
INSERT INTO "students" VALUES(9,'HV0009',NULL,NULL,'ACTIVE',5,'2026-11-04 06:27:55.879992','2026-11-04 06:27:55.879995',0);
INSERT INTO "students" VALUES(10,'HV0010',NULL,NULL,'ACTIVE',6,'2026-11-04 06:27:57.847043','2026-11-04 06:27:57.847046',0);
INSERT INTO "students" VALUES(11,'HV0011',NULL,NULL,'ACTIVE',7,'2026-11-04 06:27:58.650099','2026-11-04 06:27:58.650103',0);
CREATE TABLE teachers (
	user_id INTEGER NOT NULL, 
	teacher_code VARCHAR(50) NOT NULL, 
	specialty VARCHAR(100), 
	degree VARCHAR(100), 
	status VARCHAR(50), 
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	is_deleted BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO "teachers" VALUES(3,'GV2026-001','IELTS 8.0 & Academic Writing','Master of Applied Linguistics','ACTIVE',1,'2026-11-04 06:07:59.494782','2026-11-04 06:07:59.494785',0);
INSERT INTO "teachers" VALUES(7,'GV0007','Giảng viên Ngoại ngữ','Cử nhân Ngôn ngữ Anh','ACTIVE',2,'2026-11-04 06:17:07.981077','2026-11-04 06:17:07.981079',0);
INSERT INTO "teachers" VALUES(10,'GV0010','Giảng viên Ngoại ngữ','Cử nhân Ngôn ngữ Anh','ACTIVE',3,'2026-11-04 06:27:57.863599','2026-11-04 06:27:57.863602',0);
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
	locked_until DATETIME, 
	reset_token VARCHAR(100), 
	reset_token_expires_at DATETIME, 
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	is_deleted BOOLEAN, 
	PRIMARY KEY (id)
);
INSERT INTO "users" VALUES('admin','admin_updated@center.edu.vn','Nguyễn Văn Quản Trị Cập Nhật','$2b$12$uptKdBvbAqLvhfJRs6EVVecRjt8.9kcQ4PPUxts4zVr4GQvzpN.mO','ADMIN','0999888777',NULL,1,0,NULL,NULL,NULL,1,'2026-11-04 06:07:59.473919','2026-11-04 06:27:58.925928',0);
INSERT INTO "users" VALUES('staff','staff@center.edu.vn','Trần Thị Học Vụ (Staff)','$2b$12$VFkFfAq9UQcnB.A.yhgK8uknZX0tsV6gSTRHiqN39erLBag8WNVy6','ACADEMIC_STAFF','0912345678',NULL,1,0,NULL,NULL,NULL,2,'2026-11-04 06:07:59.473937','2026-11-04 06:07:59.473938',0);
INSERT INTO "users" VALUES('teacher','teacher@center.edu.vn','ThS. Lê Hoàng Nam (Teacher)','$2b$12$kLUYJZLYqUVZZpkWhnDYS.QWt2mRM4hCPcTmvAC9T8QsgWUmtt3tW','TEACHER','0923456789',NULL,1,0,NULL,NULL,NULL,3,'2026-11-04 06:07:59.473939','2026-11-04 06:07:59.473940',0);
INSERT INTO "users" VALUES('student','student@center.edu.vn','Phạm Minh Khang (Student)','$2b$12$ESnjS/MPYmbDDgCniifvxO9MHHNIjker5Fz2Ir05ds7yrPfJR3fgG','STUDENT','0934567890',NULL,1,0,NULL,NULL,NULL,4,'2026-11-04 06:07:59.473940','2026-11-04 06:07:59.473941',0);
INSERT INTO "users" VALUES('parent','parent@center.edu.vn','Phạm Quốc Hùng (Parent)','$2b$12$YiwnwA3fnVHuMRyvcFi1x.a81tzrGkivs3HiY1M882r9vysvDhCh6','PARENT','0945678901',NULL,1,0,NULL,NULL,NULL,5,'2026-11-04 06:07:59.473942','2026-11-04 06:07:59.473942',0);
INSERT INTO "users" VALUES('locktest_1793773025','locktest_1793773025@smartedu.edu.vn','Kiểm Thử Khóa Đăng Nhập','$2b$12$PxZ5lRN7pDnmuAMe3np/zejxizHPXmutKBPEHVOll65VOsoIU0YkS','STUDENT',NULL,NULL,1,0,NULL,NULL,NULL,6,'2026-11-04 06:17:05.768031','2026-11-04 06:17:07.428996',0);
INSERT INTO "users" VALUES('user_manage_1793773027','user_manage_1793773027@center.edu.vn','Nguyễn Quản Trị Mục Tiêu','$2b$12$odXkRgDysTTB7MmP5LbAeede/R8DeezQHwlwjhyVqBStat2sGzOQq','TEACHER','0988776655',NULL,0,0,NULL,NULL,NULL,7,'2026-11-04 06:17:07.946353','2026-11-04 06:17:08.577026',1);
INSERT INTO "users" VALUES('new_student_1793773028','new_student_1793773028@student.edu.vn','Học Viên Mới Đăng Ký','$2b$12$ZaD87crhs7PN7xe0j3hLY.4EYhKmIDAPE82ew3ZlfQOuVf4vSUwRC','STUDENT','0987654321',NULL,1,0,NULL,NULL,NULL,8,'2026-11-04 06:17:08.868684','2026-11-04 06:17:08.868689',0);
INSERT INTO "users" VALUES('locktest_1793773675','locktest_1793773675@smartedu.edu.vn','Kiểm Thử Khóa Đăng Nhập','$2b$12$RJXIzpNBV66urySuMblr0uELLe2SvVrziVS4KHa86bOohwEGdlgAy','STUDENT',NULL,NULL,1,0,NULL,NULL,NULL,9,'2026-11-04 06:27:55.867935','2026-11-04 06:27:57.356990',0);
INSERT INTO "users" VALUES('user_manage_1793773677','user_manage_1793773677@center.edu.vn','Nguyễn Quản Trị Mục Tiêu','$2b$12$g0bgvDNl57tIcIf9fsZBneaKKzuNLwzOMHF.wgKx/8vR/KoA3lVl2','TEACHER','0988776655',NULL,0,0,NULL,NULL,NULL,10,'2026-11-04 06:27:57.843642','2026-11-04 06:27:58.398273',1);
INSERT INTO "users" VALUES('new_student_1793773678','new_student_1793773678@student.edu.vn','Học Viên Mới Đăng Ký','$2b$12$p99mXhxfvQFwN9Sj1GIq6OErSUnL30FIRJHkmWLbuOUhJIpitRMnu','STUDENT','0987654321',NULL,1,0,NULL,NULL,NULL,11,'2026-11-04 06:27:58.639058','2026-11-04 06:27:58.639061',0);
CREATE UNIQUE INDEX ix_users_username ON users (username);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE INDEX ix_users_id ON users (id);
CREATE INDEX ix_courses_id ON courses (id);
CREATE UNIQUE INDEX ix_courses_code ON courses (code);
CREATE INDEX ix_classrooms_id ON classrooms (id);
CREATE UNIQUE INDEX ix_classrooms_room_code ON classrooms (room_code);
CREATE INDEX ix_students_id ON students (id);
CREATE UNIQUE INDEX ix_students_student_code ON students (student_code);
CREATE UNIQUE INDEX ix_teachers_teacher_code ON teachers (teacher_code);
CREATE INDEX ix_teachers_id ON teachers (id);
CREATE INDEX ix_classes_id ON classes (id);
CREATE UNIQUE INDEX ix_classes_class_code ON classes (class_code);
CREATE INDEX ix_course_progressions_id ON course_progressions (id);
CREATE INDEX ix_parent_students_id ON parent_students (id);
CREATE INDEX ix_class_students_id ON class_students (id);
CREATE INDEX ix_enrollment_requests_id ON enrollment_requests (id);
CREATE INDEX ix_schedule_sessions_id ON schedule_sessions (id);
CREATE INDEX ix_grade_records_id ON grade_records (id);
COMMIT;
