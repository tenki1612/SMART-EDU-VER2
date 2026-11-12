from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class EnrollmentCreate(BaseModel):
    """Học viên gửi đơn đăng ký lớp học"""
    class_id: int = Field(..., description="ID lớp học muốn đăng ký")
    note: Optional[str] = Field(None, max_length=500, description="Ghi chú gửi Phòng Học vụ (tùy chọn)")

class EnrollmentReject(BaseModel):
    """Học vụ từ chối đơn kèm lý do phản hồi"""
    rejection_reason: str = Field(..., min_length=1, max_length=500, description="Bắt buộc nhập lý do từ chối")

class EnrollmentRequestResponse(BaseModel):
    id: int
    student_id: int
    student_code: Optional[str] = None
    student_name: Optional[str] = None
    class_id: int
    class_code: Optional[str] = None
    course_title: Optional[str] = None
    request_date: Optional[datetime] = None
    status: str
    note: Optional[str] = None
    rejection_reason: Optional[str] = None
    reviewed_by: Optional[int] = None
    reviewer_name: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
