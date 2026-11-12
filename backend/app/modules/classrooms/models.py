from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.common.base_model import TimestampMixin

class Classroom(Base, TimestampMixin):
    """Cơ sở vật chất & sức chứa phòng học (bảng `classrooms`)"""
    __tablename__ = "classrooms"

    room_code = Column(String(50), unique=True, index=True, nullable=False)
    building = Column(String(50), default="Tòa nhà A")
    capacity = Column(Integer, default=30)
    status = Column(String(50), default="AVAILABLE")  # AVAILABLE, MAINTENANCE, OCCUPIED
