from sqlalchemy import Column, String, Integer, Float, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.common.base_model import TimestampMixin

class Course(Base, TimestampMixin):
    """Chương trình đào tạo & chuẩn đầu ra (bảng `courses`)"""
    __tablename__ = "courses"

    code = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    target_level = Column(String(100), nullable=False)
    duration_weeks = Column(Integer, default=12)
    fee = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
