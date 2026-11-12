from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.exceptions import BusinessException, NotFoundException, ConflictException, ForbiddenException
from app.modules.accounts.models import User
from app.modules.students.models import Student
from app.modules.courses.models import Course
from app.modules.classes.models import Class, ClassStudent
from app.modules.enrollments.models import EnrollmentRequest
from app.modules.enrollments.schemas import EnrollmentCreate, EnrollmentReject

class EnrollmentService:
    """
    FR-50 -> FR-60: Quy trình đăng ký lớp học & xét duyệt ghi danh.

    Máy trạng thái (KI-14):
        PENDING --(Student Cancel)--> CANCELLED
        PENDING --(Staff Approve)--> APPROVED
        PENDING --(Staff Reject)----> REJECTED
    """

    # -----------------------------------------------------------------
    # TIỆN ÍCH NỘI BỘ
    # -----------------------------------------------------------------
    @staticmethod
    def _get_student_by_user(db: Session, user_id: int) -> Student:
        student = db.query(Student).filter(
            Student.user_id == user_id,
            Student.is_deleted == False
        ).first()
        if not student:
            raise ForbiddenException("Tài khoản này không có hồ sơ học viên hợp lệ.")
        return student

    @staticmethod
    def _serialize(req: EnrollmentRequest, db: Session) -> dict:
        """Chuyển model -> dict phẳng (snake_case) cho frontend"""
        student = req.student
        user = student.user if student else None
        enrolled_class = req.enrolled_class
        course = enrolled_class.course if enrolled_class else None
        reviewer = req.reviewer

        return {
            "id": req.id,
            "student_id": req.student_id,
            "student_code": student.student_code if student else None,
            "student_name": user.full_name if user else (student.student_code if student else None),
            "class_id": req.class_id,
            "class_code": enrolled_class.class_code if enrolled_class else None,
            "course_title": course.title if course else None,
            "request_date": req.request_date,
            "status": req.status,
            "note": req.note,
            "rejection_reason": req.rejection_reason,
            "reviewed_by": req.reviewed_by,
            "reviewer_name": reviewer.full_name if reviewer else None,
            "reviewed_at": req.reviewed_at,
            "created_at": req.created_at,
        }

    @staticmethod
    def _serialize_class(cls: Class, db: Session, student: Optional[Student] = None) -> dict:
        """Thông tin lớp học mở đăng ký (dùng cho học viên chọn lớp)"""
        course = cls.course
        teacher = cls.teacher
        teacher_name = teacher.user.full_name if teacher and teacher.user else None
        is_enrolled = False
        if student is not None:
            existing = db.query(ClassStudent).filter(
                ClassStudent.class_id == cls.id,
                ClassStudent.student_id == student.id,
                ClassStudent.is_deleted == False
            ).first()
            is_enrolled = existing is not None

        return {
            "id": cls.id,
            "class_code": cls.class_code,
            "course_id": cls.course_id,
            "course_title": course.title if course else None,
            "target_level": course.target_level if course else None,
            "teacher_id": cls.teacher_id,
            "teacher_name": teacher_name,
            "max_capacity": cls.max_capacity,
            "current_enrolled": cls.current_enrolled,
            "is_full": cls.current_enrolled >= cls.max_capacity,
            "is_enrolled": is_enrolled,
            "start_date": cls.start_date,
            "end_date": cls.end_date,
            "status": cls.status,
        }

    # -----------------------------------------------------------------
    # FR-50 / FR-51: HỌC VIÊN XEM LỚP ĐANG MỞ & GỬI ĐƠN ĐĂNG KÝ
    # -----------------------------------------------------------------
    @staticmethod
    def list_open_classes(db: Session, user_id: int) -> List[dict]:
        """Danh sách lớp đang mở tuyển sinh kèm trạng thái đã đăng ký của học viên"""
        student = EnrollmentService._get_student_by_user(db, user_id)
        classes = db.query(Class).filter(
            Class.is_deleted == False,
            Class.status == "OPEN_FOR_ENROLLMENT"
        ).order_by(Class.id).all()
        return [EnrollmentService._serialize_class(c, db, student) for c in classes]

    @staticmethod
    def create_request(db: Session, user_id: int, data: EnrollmentCreate) -> dict:
        """Học viên gửi yêu cầu đăng ký vào một lớp học"""
        student = EnrollmentService._get_student_by_user(db, user_id)

        enrolled_class = db.query(Class).filter(
            Class.id == data.class_id,
            Class.is_deleted == False
        ).first()
        if not enrolled_class:
            raise NotFoundException("Lớp học", data.class_id)

        if enrolled_class.status != "OPEN_FOR_ENROLLMENT":
            raise BusinessException(f"Lớp học '{enrolled_class.class_code}' hiện không mở đăng ký.")

        # Chặn đơn trùng: 1 học viên chỉ có 1 đơn PENDING cho 1 lớp
        duplicate = db.query(EnrollmentRequest).filter(
            EnrollmentRequest.student_id == student.id,
            EnrollmentRequest.class_id == enrolled_class.id,
            EnrollmentRequest.status == "PENDING",
            EnrollmentRequest.is_deleted == False
        ).first()
        if duplicate:
            raise ConflictException("Bạn đã có một đơn đăng ký đang chờ duyệt cho lớp học này.")

        # Chặn đăng ký lại khi đã ghi danh vào lớp
        already = db.query(ClassStudent).filter(
            ClassStudent.class_id == enrolled_class.id,
            ClassStudent.student_id == student.id,
            ClassStudent.is_deleted == False
        ).first()
        if already:
            raise ConflictException("Bạn đã được ghi danh vào lớp học này.")

        request = EnrollmentRequest(
            student_id=student.id,
            class_id=enrolled_class.id,
            request_date=datetime.now(timezone.utc),
            status="PENDING",
            note=data.note
        )
        db.add(request)
        db.commit()
        db.refresh(request)
        return EnrollmentService._serialize(request, db)

    @staticmethod
    def list_my_requests(db: Session, user_id: int) -> List[dict]:
        """Học viên xem toàn bộ đơn đăng ký của chính mình"""
        student = EnrollmentService._get_student_by_user(db, user_id)
        requests = db.query(EnrollmentRequest).filter(
            EnrollmentRequest.student_id == student.id,
            EnrollmentRequest.is_deleted == False
        ).order_by(EnrollmentRequest.id.desc()).all()
        return [EnrollmentService._serialize(r, db) for r in requests]

    @staticmethod
    def cancel_request(db: Session, request_id: int, user_id: int) -> dict:
        """Học viên tự hủy đơn — chỉ được hủy khi đơn còn PENDING (KI-14)"""
        student = EnrollmentService._get_student_by_user(db, user_id)
        request = db.query(EnrollmentRequest).filter(
            EnrollmentRequest.id == request_id,
            EnrollmentRequest.is_deleted == False
        ).first()
        if not request:
            raise NotFoundException("Đơn đăng ký", request_id)

        if request.student_id != student.id:
            raise ForbiddenException("Bạn chỉ có thể hủy đơn đăng ký của chính mình.")

        if request.status != "PENDING":
            if request.status == "APPROVED":
                raise BusinessException(
                    "Đơn đăng ký đã được phê duyệt và bạn đã ghi danh vào lớp. "
                    "Vui lòng liên hệ Phòng Học vụ để thực hiện thủ tục rút lớp."
                )
            raise BusinessException("Chỉ có thể hủy yêu cầu khi đang ở trạng thái 'Chờ duyệt' (PENDING).")

        request.status = "CANCELLED"
        request.reviewed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(request)
        return EnrollmentService._serialize(request, db)

    # -----------------------------------------------------------------
    # FR-52 -> FR-57: HỌC VỤ XÉT DUYỆT
    # -----------------------------------------------------------------
    @staticmethod
    def list_all_requests(db: Session, status: Optional[str] = None) -> List[dict]:
        """Học vụ / Admin xem toàn bộ đơn đăng ký trong hệ thống"""
        q = db.query(EnrollmentRequest).filter(EnrollmentRequest.is_deleted == False)
        if status and status != "ALL":
            q = q.filter(EnrollmentRequest.status == status)
        requests = q.order_by(EnrollmentRequest.id.desc()).all()
        return [EnrollmentService._serialize(r, db) for r in requests]

    @staticmethod
    def approve_request(db: Session, request_id: int, reviewer_user_id: int) -> dict:
        """Phê duyệt đơn: ghi danh vào class_students và tăng current_enrolled"""
        request = db.query(EnrollmentRequest).filter(
            EnrollmentRequest.id == request_id,
            EnrollmentRequest.is_deleted == False
        ).first()
        if not request:
            raise NotFoundException("Đơn đăng ký", request_id)

        if request.status != "PENDING":
            raise BusinessException(f"Đơn đăng ký #{request_id} đã được xử lý (trạng thái: {request.status}).")

        enrolled_class = request.enrolled_class
        if not enrolled_class:
            raise NotFoundException("Lớp học", request.class_id)

        # Ràng buộc sĩ số tối đa
        if enrolled_class.current_enrolled >= enrolled_class.max_capacity:
            raise BusinessException(
                f"Lớp học '{enrolled_class.class_code}' đã đầu sĩ số "
                f"({enrolled_class.current_enrolled}/{enrolled_class.max_capacity}). "
                "Vui lòng từ chối đơn hoặc tăng sức chứa lớp trước khi phê duyệt."
            )

        # Ghi danh vào lớp (tránh trùng bản ghi)
        enrolled = db.query(ClassStudent).filter(
            ClassStudent.class_id == enrolled_class.id,
            ClassStudent.student_id == request.student_id
        ).first()
        if enrolled:
            enrolled.is_deleted = False
            enrolled.status = "ENROLLED"
        else:
            db.add(ClassStudent(
                class_id=enrolled_class.id,
                student_id=request.student_id,
                enrolled_at=datetime.now(timezone.utc),
                status="ENROLLED"
            ))

        enrolled_class.current_enrolled = (enrolled_class.current_enrolled or 0) + 1
        request.status = "APPROVED"
        request.reviewed_by = reviewer_user_id
        request.reviewed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(request)
        return EnrollmentService._serialize(request, db)

    @staticmethod
    def reject_request(db: Session, request_id: int, reviewer_user_id: int, data: EnrollmentReject) -> dict:
        """Từ chối đơn — bắt buộc kèm lý do phản hồi cho học viên"""
        request = db.query(EnrollmentRequest).filter(
            EnrollmentRequest.id == request_id,
            EnrollmentRequest.is_deleted == False
        ).first()
        if not request:
            raise NotFoundException("Đơn đăng ký", request_id)

        if request.status != "PENDING":
            raise BusinessException(f"Đơn đăng ký #{request_id} đã được xử lý (trạng thái: {request.status}).")

        reason = (data.rejection_reason or "").strip()
        if not reason:
            raise BusinessException("Bắt buộc nhập lý do từ chối để thông báo cho học viên.")

        request.status = "REJECTED"
        request.rejection_reason = reason
        request.reviewed_by = reviewer_user_id
        request.reviewed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(request)
        return EnrollmentService._serialize(request, db)
