from datetime import date, datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import BusinessException, NotFoundException, ForbiddenException
from app.modules.accounts.models import User
from app.modules.classes.models import Class
from app.modules.classrooms.models import Classroom
from app.modules.teachers.models import Teacher
from app.modules.students.models import Student
from app.modules.classes.models import ClassStudent
from app.modules.schedules.models import ScheduleSession
from app.modules.schedules.schemas import ScheduleCreate, ScheduleUpdate, ConflictCheck, ConflictItem
from app.modules.schedules.conflict_checker import (
    is_time_overlap,
    is_valid_time_range,
    describe_conflict,
)


class ScheduleService:
    """
    FR-61 -> FR-68: Quản lý thời khóa biểu & thuật toán phát hiện xung đột.

    Xung đột được kiểm tra trên 2 tài nguyên (KI-01):
      - Phòng học (classroom_id): 2 lớp không được dùng chung phòng cùng khung giờ.
      - Giáo viên (teacher_id): 1 giáo viên không được dạy 2 lớp cùng khung giờ.
    """

    # -----------------------------------------------------------------
    # TIỆN ÍCH NỘI BỘ
    # -----------------------------------------------------------------
    @staticmethod
    def _serialize(session: ScheduleSession) -> dict:
        enrolled_class = session.session_class
        course = enrolled_class.course if enrolled_class else None
        classroom = session.classroom
        teacher = session.teacher
        teacher_name = teacher.user.full_name if teacher and teacher.user else None
        return {
            "id": session.id,
            "class_id": session.class_id,
            "class_code": enrolled_class.class_code if enrolled_class else None,
            "course_title": course.title if course else None,
            "classroom_id": session.classroom_id,
            "room_code": classroom.room_code if classroom else None,
            "building": classroom.building if classroom else None,
            "teacher_id": session.teacher_id,
            "teacher_name": teacher_name,
            "session_date": session.session_date,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "slot_name": session.slot_name,
            "is_confirmed": session.is_confirmed,
            "status": session.status,
            "created_at": session.created_at,
        }

    @staticmethod
    def _get_class(db: Session, class_id: int) -> Class:
        enrolled_class = db.query(Class).filter(
            Class.id == class_id,
            Class.is_deleted == False
        ).first()
        if not enrolled_class:
            raise NotFoundException("Lớp học", class_id)
        return enrolled_class

    @staticmethod
    def _get_classroom(db: Session, classroom_id: int) -> Classroom:
        classroom = db.query(Classroom).filter(
            Classroom.id == classroom_id,
            Classroom.is_deleted == False
        ).first()
        if not classroom:
            raise NotFoundException("Phòng học", classroom_id)
        return classroom

    @staticmethod
    def _get_teacher(db: Session, teacher_id: int) -> Teacher:
        teacher = db.query(Teacher).filter(
            Teacher.id == teacher_id,
            Teacher.is_deleted == False
        ).first()
        if not teacher:
            raise NotFoundException("Giáo viên", teacher_id)
        return teacher

    @staticmethod
    def _default_slot_name(start_time: str, end_time: str) -> str:
        return f"Ca học ({start_time} - {end_time})"

    # -----------------------------------------------------------------
    # FR-62 / FR-65: THUẬT TOÁN PHÁT HIỆN XUNG ĐỘT
    # -----------------------------------------------------------------
    @staticmethod
    def detect_conflicts(
        db: Session,
        classroom_id: int,
        teacher_id: int,
        session_date: date,
        start_time: str,
        end_time: str,
        exclude_session_id: Optional[int] = None
    ) -> List[ConflictItem]:
        """
        Quét các buổi học cùng ngày và trả về danh sách xung đột.

        - Bỏ qua buổi đã hủy (status == 'CANCELLED') và đã soft-delete.
        - Loại trừ chính buổi đang sửa (exclude_session_id).
        """
        if not is_valid_time_range(start_time, end_time):
            raise BusinessException("Giờ kết thúc buổi học phải lớn hơn giờ bắt đầu.")

        candidates = db.query(ScheduleSession).filter(
            ScheduleSession.session_date == session_date,
            ScheduleSession.is_deleted == False,
            ScheduleSession.status != "CANCELLED"
        )
        if exclude_session_id:
            candidates = candidates.filter(ScheduleSession.id != exclude_session_id)

        conflicts: List[ConflictItem] = []
        for other in candidates.all():
            same_classroom = other.classroom_id == classroom_id
            same_teacher = other.teacher_id == teacher_id
            if not same_classroom and not same_teacher:
                continue
            if not is_time_overlap(start_time, end_time, other.start_time, other.end_time):
                continue

            enrolled_class = other.session_class
            course = enrolled_class.course if enrolled_class else None
            classroom = other.classroom
            teacher = other.teacher
            teacher_name = teacher.user.full_name if teacher and teacher.user else None

            if same_classroom:
                conflict_type = "CLASSROOM"
                message = describe_conflict(
                    "CLASSROOM",
                    classroom_code=classroom.room_code if classroom else "",
                    teacher_name=teacher_name or "",
                    class_code=enrolled_class.class_code if enrolled_class else "",
                    start_time=other.start_time,
                    end_time=other.end_time,
                )
            else:
                conflict_type = "TEACHER"
                message = describe_conflict(
                    "TEACHER",
                    classroom_code=classroom.room_code if classroom else "",
                    teacher_name=teacher_name or "",
                    class_code=enrolled_class.class_code if enrolled_class else "",
                    start_time=other.start_time,
                    end_time=other.end_time,
                )

            conflicts.append(ConflictItem(
                conflict_type=conflict_type,
                session_id=other.id,
                class_code=enrolled_class.class_code if enrolled_class else None,
                course_title=course.title if course else None,
                classroom_id=other.classroom_id,
                room_code=classroom.room_code if classroom else None,
                teacher_id=other.teacher_id,
                teacher_name=teacher_name,
                session_date=other.session_date,
                start_time=other.start_time,
                end_time=other.end_time,
                message=message,
            ))
        return conflicts

    @staticmethod
    def check_conflict(db: Session, data: ConflictCheck) -> dict:
        """Kiểm tra xung đột trước khi lưu (FR-65)"""
        conflicts = ScheduleService.detect_conflicts(
            db,
            classroom_id=data.classroom_id,
            teacher_id=data.teacher_id,
            session_date=data.session_date,
            start_time=data.start_time,
            end_time=data.end_time,
            exclude_session_id=data.exclude_session_id,
        )
        if not conflicts:
            return {
                "has_conflict": False,
                "conflict_type": None,
                "message": "Lịch học hợp lệ, không có xung đột về phòng học hoặc giáo viên.",
                "conflicts": [],
            }

        first = conflicts[0]
        summary = first.message
        if len(conflicts) > 1:
            summary += f" (phát hiện {len(conflicts)} xung đột)"
        return {
            "has_conflict": True,
            "conflict_type": first.conflict_type,
            "message": summary,
            "conflicts": conflicts,
        }

    @staticmethod
    def _assert_no_conflict(
        db: Session,
        classroom_id: int,
        teacher_id: int,
        session_date: date,
        start_time: str,
        end_time: str,
        exclude_session_id: Optional[int] = None
    ):
        """Chặn lưu khi còn xung đột chưa được xử lý (FR-64)"""
        conflicts = ScheduleService.detect_conflicts(
            db,
            classroom_id=classroom_id,
            teacher_id=teacher_id,
            session_date=session_date,
            start_time=start_time,
            end_time=end_time,
            exclude_session_id=exclude_session_id,
        )
        if conflicts:
            raise BusinessException(f"Không thể lưu buổi học do xung đột lịch: {conflicts[0].message}")

    # -----------------------------------------------------------------
    # FR-61: XEM THỜI KHÓA BIỂU
    # -----------------------------------------------------------------
    @staticmethod
    def list_sessions(
        db: Session,
        class_id: Optional[int] = None,
        teacher_id: Optional[int] = None
    ) -> List[dict]:
        """Lấy toàn bộ lịch học (Admin / Học vụ)"""
        query = db.query(ScheduleSession).filter(ScheduleSession.is_deleted == False)
        if class_id:
            query = query.filter(ScheduleSession.class_id == class_id)
        if teacher_id:
            query = query.filter(ScheduleSession.teacher_id == teacher_id)
        sessions = query.order_by(
            ScheduleSession.session_date,
            ScheduleSession.start_time
        ).all()
        return [ScheduleService._serialize(s) for s in sessions]

    @staticmethod
    def list_personal_sessions(db: Session, user_id: int, role: str) -> List[dict]:
        """Lịch học cá nhân của Giáo viên hoặc Học viên đang đăng nhập (FR-63)"""
        query = db.query(ScheduleSession).filter(ScheduleSession.is_deleted == False)

        if role == "TEACHER":
            teacher = db.query(Teacher).filter(
                Teacher.user_id == user_id,
                Teacher.is_deleted == False
            ).first()
            if not teacher:
                raise ForbiddenException("Tài khoản này không có hồ sơ giảng viên hợp lệ.")
            query = query.filter(ScheduleSession.teacher_id == teacher.id)
        elif role == "STUDENT":
            student = db.query(Student).filter(
                Student.user_id == user_id,
                Student.is_deleted == False
            ).first()
            if not student:
                raise ForbiddenException("Tài khoản này không có hồ sơ học viên hợp lệ.")
            enrolled_class_ids = [
                row.class_id
                for row in db.query(ClassStudent).filter(
                    ClassStudent.student_id == student.id,
                    ClassStudent.is_deleted == False
                ).all()
            ]
            if not enrolled_class_ids:
                return []
            query = query.filter(ScheduleSession.class_id.in_(enrolled_class_ids))
        else:
            raise ForbiddenException("Chức năng này chỉ dành cho Giáo viên hoặc Học viên.")

        sessions = query.order_by(
            ScheduleSession.session_date,
            ScheduleSession.start_time
        ).all()
        return [ScheduleService._serialize(s) for s in sessions]

    # -----------------------------------------------------------------
    # FR-63 / FR-64: TẠO & CẬP NHẬT BUỔI HỌC
    # -----------------------------------------------------------------
    @staticmethod
    def create_session(db: Session, data: ScheduleCreate) -> dict:
        enrolled_class = ScheduleService._get_class(db, data.class_id)
        classroom = ScheduleService._get_classroom(db, data.classroom_id)
        ScheduleService._get_teacher(db, data.teacher_id)

        if classroom.status == "MAINTENANCE":
            raise BusinessException(
                f"Phòng học {classroom.room_code} đang bảo trì, không thể xếp lịch học."
            )

        if not is_valid_time_range(data.start_time, data.end_time):
            raise BusinessException("Giờ kết thúc buổi học phải lớn hơn giờ bắt đầu.")

        ScheduleService._assert_no_conflict(
            db,
            classroom_id=data.classroom_id,
            teacher_id=data.teacher_id,
            session_date=data.session_date,
            start_time=data.start_time,
            end_time=data.end_time,
        )

        session = ScheduleSession(
            class_id=enrolled_class.id,
            classroom_id=classroom.id,
            teacher_id=data.teacher_id,
            session_date=data.session_date,
            start_time=data.start_time,
            end_time=data.end_time,
            slot_name=data.slot_name or ScheduleService._default_slot_name(
                data.start_time, data.end_time
            ),
            is_confirmed=False,
            status="SCHEDULED",
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return ScheduleService._serialize(session)

    @staticmethod
    def update_session(db: Session, session_id: int, data: ScheduleUpdate) -> dict:
        session = db.query(ScheduleSession).filter(
            ScheduleSession.id == session_id,
            ScheduleSession.is_deleted == False
        ).first()
        if not session:
            raise NotFoundException("Buổi học", session_id)

        if session.status == "CANCELLED":
            raise BusinessException("Buổi học đã hủy, không thể điều chỉnh.")

        classroom_id = data.classroom_id if data.classroom_id is not None else session.classroom_id
        teacher_id = data.teacher_id if data.teacher_id is not None else session.teacher_id
        session_date = data.session_date if data.session_date is not None else session.session_date
        start_time = data.start_time if data.start_time is not None else session.start_time
        end_time = data.end_time if data.end_time is not None else session.end_time

        classroom = ScheduleService._get_classroom(db, classroom_id)
        if classroom.status == "MAINTENANCE":
            raise BusinessException(
                f"Phòng học {classroom.room_code} đang bảo trì, không thể xếp lịch học."
            )

        if not is_valid_time_range(start_time, end_time):
            raise BusinessException("Giờ kết thúc buổi học phải lớn hơn giờ bắt đầu.")

        ScheduleService._assert_no_conflict(
            db,
            classroom_id=classroom_id,
            teacher_id=teacher_id,
            session_date=session_date,
            start_time=start_time,
            end_time=end_time,
            exclude_session_id=session.id,
        )

        session.classroom_id = classroom_id
        session.teacher_id = teacher_id
        session.session_date = session_date
        session.start_time = start_time
        session.end_time = end_time
        if data.slot_name is not None:
            session.slot_name = data.slot_name
        if data.status is not None:
            # Frontend dùng 'ACTIVE' cho ca đang hoạt động -> quy đổi về SCHEDULED
            normalized_status = "SCHEDULED" if data.status == "ACTIVE" else data.status
            if normalized_status not in ("SCHEDULED", "COMPLETED", "CANCELLED"):
                raise BusinessException("Trạng thái buổi học không hợp lệ.")
            session.status = normalized_status
        db.commit()
        db.refresh(session)
        return ScheduleService._serialize(session)

    # -----------------------------------------------------------------
    # FR-66 / FR-67: HỦY & XÓA
    # -----------------------------------------------------------------
    @staticmethod
    def cancel_session(db: Session, session_id: int) -> dict:
        session = db.query(ScheduleSession).filter(
            ScheduleSession.id == session_id,
            ScheduleSession.is_deleted == False
        ).first()
        if not session:
            raise NotFoundException("Buổi học", session_id)
        if session.status == "CANCELLED":
            raise BusinessException("Buổi học này đã được hủy trước đó.")
        session.status = "CANCELLED"
        db.commit()
        db.refresh(session)
        return ScheduleService._serialize(session)

    @staticmethod
    def delete_session(db: Session, session_id: int) -> bool:
        session = db.query(ScheduleSession).filter(
            ScheduleSession.id == session_id,
            ScheduleSession.is_deleted == False
        ).first()
        if not session:
            raise NotFoundException("Buổi học", session_id)
        session.is_deleted = True
        db.commit()
        return True

    # -----------------------------------------------------------------
    # FR-68: XÁC NHẬN THỜI KHÓA BIỂU CHÍNH THỨC
    # -----------------------------------------------------------------
    @staticmethod
    def confirm_class_schedule(db: Session, class_id: int) -> dict:
        enrolled_class = ScheduleService._get_class(db, class_id)
        sessions = db.query(ScheduleSession).filter(
            ScheduleSession.class_id == enrolled_class.id,
            ScheduleSession.is_deleted == False,
            ScheduleSession.status != "CANCELLED"
        ).all()
        if not sessions:
            raise BusinessException(
                f"Lớp {enrolled_class.class_code} chưa có buổi học nào để xác nhận."
            )
        for session in sessions:
            session.is_confirmed = True
        db.commit()
        return {
            "class_id": enrolled_class.id,
            "class_code": enrolled_class.class_code,
            "confirmed_count": len(sessions),
            "message": f"Đã xác nhận {len(sessions)} buổi học của lớp {enrolled_class.class_code}.",
        }
