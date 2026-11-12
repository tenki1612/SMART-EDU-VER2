from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.common.base_model import TimestampMixin

class EnrollmentRequest(Base, TimestampMixin):
    """Đơn đăng ký lớp học & xét duyệt ghi danh (bảng `enrollment_requests`)"""
    __tablename__ = "enrollment_requests"

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False, index=True)
    request_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String(50), default="PENDING", index=True)  # PENDING, APPROVED, REJECTED, CANCELLED
    note = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    reviewed_at = Column(DateTime, nullable=True)

    # Relationships
    student = relationship("Student", foreign_keys=[student_id])
    enrolled_class = relationship("Class", foreign_keys=[class_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
