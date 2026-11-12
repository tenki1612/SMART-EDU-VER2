from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.common.base_model import TimestampMixin

class Class(Base, TimestampMixin):
    """Lớp học mở theo khóa đào tạo (bảng `classes`)"""
    __tablename__ = "classes"

    class_code = Column(String(50), unique=True, index=True, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True, index=True)
    max_capacity = Column(Integer, default=25)
    current_enrolled = Column(Integer, default=0)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String(50), default="OPEN_FOR_ENROLLMENT")

    # Relationships
    course = relationship("Course", foreign_keys=[course_id])
    teacher = relationship("Teacher", foreign_keys=[teacher_id])

class ClassStudent(Base, TimestampMixin):
    """Danh sách học viên trong lớp (bảng `class_students`)"""
    __tablename__ = "class_students"

    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    enrolled_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String(50), default="ENROLLED")

    # Relationships
    enrolled_class = relationship("Class", foreign_keys=[class_id])
    student = relationship("Student", foreign_keys=[student_id])
