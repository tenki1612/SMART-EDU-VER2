from datetime import date, datetime, timezone
from sqlalchemy import Column, String, Integer, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.common.base_model import TimestampMixin

class ScheduleSession(Base, TimestampMixin):
    """Lịch học từng buổi, xếp phòng & giáo viên (bảng `schedule_sessions`)"""
    __tablename__ = "schedule_sessions"

    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False, index=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False, index=True)
    session_date = Column(Date, nullable=False, index=True)
    start_time = Column(String(10), nullable=False)  # "18:00"
    end_time = Column(String(10), nullable=False)    # "20:00"
    slot_name = Column(String(50), default="Ca tối (18:00 - 20:00)")
    is_confirmed = Column(Boolean, default=False)
    status = Column(String(50), default="SCHEDULED")  # SCHEDULED, COMPLETED, CANCELLED

    # Relationships
    session_class = relationship("Class", foreign_keys=[class_id])
    classroom = relationship("Classroom", foreign_keys=[classroom_id])
    teacher = relationship("Teacher", foreign_keys=[teacher_id])
