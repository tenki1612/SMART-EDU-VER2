from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.common.base_model import TimestampMixin

class Student(Base, TimestampMixin):
    __tablename__ = "students"

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    student_code = Column(String(50), unique=True, index=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    address = Column(String(255), nullable=True)
    status = Column(String(50), default="ACTIVE")

    # Relationships
    user = relationship("User", back_populates="student_profile")
    parents = relationship("ParentStudent", foreign_keys="ParentStudent.student_id", back_populates="student")
