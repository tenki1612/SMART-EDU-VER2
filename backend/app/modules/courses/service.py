from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.exceptions import BusinessException, NotFoundException, ConflictException
from app.modules.courses.models import Course
from app.modules.courses.schemas import CourseCreate, CourseUpdate
from app.modules.classes.models import Class


class CourseService:
    """
    FR-11 -> FR-16: Quản lý Khóa đào tạo & Biểu phí chuẩn (Courses Context).
    """

    @staticmethod
    def list_courses(
        db: Session,
        q: Optional[str] = None,
        only_active: bool = False,
        target_level: Optional[str] = None
    ) -> List[Course]:
        """Tra cứu danh sách khóa học có hỗ trợ tìm kiếm và lọc."""
        query = db.query(Course).filter(Course.is_deleted == False)

        if only_active:
            query = query.filter(Course.is_active == True)

        if q and q.strip():
            term = f"%{q.strip()}%"
            query = query.filter(
                or_(
                    Course.title.ilike(term),
                    Course.code.ilike(term),
                    Course.target_level.ilike(term),
                    Course.description.ilike(term),
                )
            )

        if target_level and target_level.strip() and target_level.upper() != "ALL":
            lvl = target_level.strip()
            query = query.filter(Course.target_level.ilike(f"%{lvl}%"))

        return query.order_by(Course.id.asc()).all()

    @staticmethod
    def get_by_id(db: Session, course_id: int) -> Course:
        """Lấy chi tiết khóa học theo ID."""
        course = db.query(Course).filter(
            Course.id == course_id,
            Course.is_deleted == False
        ).first()
        if not course:
            raise NotFoundException("Khóa học", course_id)
        return course

    @staticmethod
    def get_by_code(db: Session, code: str) -> Optional[Course]:
        """Lấy thông tin khóa học theo Mã định danh."""
        return db.query(Course).filter(
            Course.code == code.strip().upper(),
            Course.is_deleted == False
        ).first()

    @staticmethod
    def create_course(db: Session, data: CourseCreate) -> Course:
        """Tạo khóa học mới kèm xác thực nghiệp vụ."""
        clean_code = data.code.strip().upper()
        clean_title = data.title.strip()

        # Kiểm tra trùng lặp mã khóa học
        existing = db.query(Course).filter(
            Course.code == clean_code,
            Course.is_deleted == False
        ).first()
        if existing:
            raise ConflictException(f"Mã khóa học '{clean_code}' đã tồn tại trong hệ thống.")

        # Ràng buộc số tuần và học phí
        if data.duration_weeks <= 0:
            raise BusinessException("Thời lượng khóa học phải lớn hơn 0 tuần.")
        if data.fee < 0:
            raise BusinessException("Học phí không thể là giá trị âm.")

        course = Course(
            code=clean_code,
            title=clean_title,
            description=data.description.strip() if data.description else None,
            target_level=data.target_level.strip(),
            duration_weeks=data.duration_weeks,
            fee=float(data.fee),
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            is_deleted=False
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def update_course(db: Session, course_id: int, data: CourseUpdate) -> Course:
        """Cập nhật thông tin khóa học."""
        course = CourseService.get_by_id(db, course_id)

        if data.title is not None:
            clean_title = data.title.strip()
            if not clean_title:
                raise BusinessException("Tên khóa học không được để trống.")
            course.title = clean_title

        if data.description is not None:
            course.description = data.description.strip() if data.description else None

        if data.target_level is not None:
            clean_level = data.target_level.strip()
            if not clean_level:
                raise BusinessException("Chuẩn đầu ra không được để trống.")
            course.target_level = clean_level

        if data.duration_weeks is not None:
            if data.duration_weeks <= 0:
                raise BusinessException("Thời lượng khóa học phải lớn hơn 0 tuần.")
            course.duration_weeks = data.duration_weeks

        if data.fee is not None:
            if data.fee < 0:
                raise BusinessException("Học phí không thể là giá trị âm.")
            course.fee = float(data.fee)

        if data.is_active is not None:
            course.is_active = data.is_active

        course.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def toggle_status(db: Session, course_id: int) -> Course:
        """Bật/tắt trạng thái kích hoạt khóa học."""
        course = CourseService.get_by_id(db, course_id)
        course.is_active = not course.is_active
        course.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def delete_course(db: Session, course_id: int) -> bool:
        """
        Xóa mềm khóa học (Soft delete).
        Bảo vệ toàn vẹn dữ liệu: Không cho phép xóa nếu đang có lớp học mở/liên kết.
        """
        course = CourseService.get_by_id(db, course_id)

        # Kiểm tra lớp học liên kết
        active_classes_count = db.query(Class).filter(
            Class.course_id == course_id,
            Class.is_deleted == False
        ).count()

        if active_classes_count > 0:
            raise BusinessException(
                f"Không thể xóa khóa học '{course.title}' vì đang có {active_classes_count} lớp học "
                "liên kết trong hệ thống. Vui lòng chuyển trạng thái Không kích hoạt (Deactivate) thay vì xóa."
            )

        course.is_deleted = True
        course.is_active = False
        course.updated_at = datetime.now(timezone.utc)
        db.commit()
        return True
