from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.classes.models import Class
from app.modules.classrooms.models import Classroom
from app.modules.courses.models import Course
from app.modules.teachers.models import Teacher


class ReferenceDataService:
    """
    Dữ liệu tham chiếu cho form xếp lịch (phòng học, giáo viên, lớp học, khóa học).

    Phân hệ `schedules` (FR-61 -> FR-68) cần 4 danh sách này để người dùng chọn
    trong Modal "Thêm buổi học". Các phân hệ `classrooms` (#7), `teachers` (#5),
    `classes` (#6), `courses` (#3) sẽ cung cấp endpoint danh sách riêng;
    endpoint này cung cấp dữ liệu tối thiểu để phân hệ lịch dùng độc lập.
    """

    @staticmethod
    def list_classrooms(db: Session) -> List[dict]:
        rooms = db.query(Classroom).filter(
            Classroom.is_deleted == False,
            Classroom.status != "MAINTENANCE"
        ).order_by(Classroom.room_code).all()
        return [
            {
                "id": r.id,
                "room_code": r.room_code,
                "building": r.building,
                "capacity": r.capacity,
                "status": r.status,
            }
            for r in rooms
        ]

    @staticmethod
    def list_teachers(db: Session) -> List[dict]:
        teachers = db.query(Teacher).filter(
            Teacher.is_deleted == False,
            Teacher.status == "ACTIVE"
        ).order_by(Teacher.teacher_code).all()
        return [
            {
                "id": t.id,
                "user_id": t.user_id,
                "teacher_code": t.teacher_code,
                "full_name": t.user.full_name if t.user else t.teacher_code,
                "specialty": t.specialty,
                "degree": t.degree,
                "status": t.status,
            }
            for t in teachers
        ]

    @staticmethod
    def list_classes(db: Session) -> List[dict]:
        classes = db.query(Class).filter(Class.is_deleted == False).order_by(Class.class_code).all()
        result = []
        for c in classes:
            course = c.course
            teacher = c.teacher
            result.append({
                "id": c.id,
                "class_code": c.class_code,
                "course_id": c.course_id,
                "course_title": course.title if course else None,
                "target_level": course.target_level if course else None,
                "teacher_id": c.teacher_id,
                "teacher_name": teacher.user.full_name if teacher and teacher.user else None,
                "max_capacity": c.max_capacity or 0,
                "current_enrolled": c.current_enrolled or 0,
                "status": c.status,
            })
        return result

    @staticmethod
    def list_courses(db: Session) -> List[dict]:
        courses = db.query(Course).filter(
            Course.is_deleted == False,
            Course.is_active == True
        ).order_by(Course.code).all()
        return [
            {
                "id": c.id,
                "code": c.code,
                "title": c.title,
                "target_level": c.target_level,
                "duration_weeks": c.duration_weeks,
                "fee": c.fee,
            }
            for c in courses
        ]

    @staticmethod
    def get_all(db: Session) -> dict:
        return {
            "classrooms": ReferenceDataService.list_classrooms(db),
            "teachers": ReferenceDataService.list_teachers(db),
            "classes": ReferenceDataService.list_classes(db),
            "courses": ReferenceDataService.list_courses(db),
        }
