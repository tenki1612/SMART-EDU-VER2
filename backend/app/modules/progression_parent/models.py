from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.common.base_model import TimestampMixin

class ParentStudent(Base, TimestampMixin):
    """Liên kết Phụ huynh và Học viên được giám hộ (FR-81, FR-82)"""
    __tablename__ = "parent_students"

    parent_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    relationship_type = Column(String(50), default="Phụ huynh / Người giám hộ")

    # Relationships
    parent_user = relationship("User", foreign_keys=[parent_user_id], back_populates="parent_links")
    student = relationship("Student", foreign_keys=[student_id], back_populates="parents")
