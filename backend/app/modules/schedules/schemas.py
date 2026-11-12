from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field

class ScheduleCreate(BaseModel):
    """Tạo buổi học mới trong thời khóa biểu"""
    class_id: int = Field(..., description="ID lớp học")
    classroom_id: int = Field(..., description="ID phòng học")
    teacher_id: int = Field(..., description="ID giáo viên phụ trách")
    session_date: date = Field(..., description="Ngày học (YYYY-MM-DD)")
    start_time: str = Field(..., pattern=r"^\d{2}:\d{2}$", description="Giờ bắt đầu (HH:MM)")
    end_time: str = Field(..., pattern=r"^\d{2}:\d{2}$", description="Giờ kết thúc (HH:MM)")
    slot_name: Optional[str] = Field(None, max_length=50, description="Tên ca học")

class ScheduleUpdate(BaseModel):
    """Điều chỉnh buổi học cụ thể"""
    classroom_id: Optional[int] = None
    teacher_id: Optional[int] = None
    session_date: Optional[date] = None
    start_time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    end_time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    slot_name: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, description="SCHEDULED, COMPLETED, CANCELLED")

class ConflictCheck(BaseModel):
    """Kiểm tra xung đột lịch trước khi lưu"""
    classroom_id: int
    teacher_id: int
    session_date: date
    start_time: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    end_time: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    exclude_session_id: Optional[int] = Field(None, description="Loại trừ chính buổi đang sửa")

class ConflictItem(BaseModel):
    conflict_type: str          # CLASSROOM | TEACHER
    session_id: int
    class_code: Optional[str] = None
    course_title: Optional[str] = None
    classroom_id: Optional[int] = None
    room_code: Optional[str] = None
    teacher_id: Optional[int] = None
    teacher_name: Optional[str] = None
    session_date: Optional[date] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    message: str

class ConflictCheckResponse(BaseModel):
    has_conflict: bool
    conflict_type: Optional[str] = None
    message: str
    conflicts: list[ConflictItem] = []

class ScheduleResponse(BaseModel):
    id: int
    class_id: int
    class_code: Optional[str] = None
    course_title: Optional[str] = None
    classroom_id: int
    room_code: Optional[str] = None
    building: Optional[str] = None
    teacher_id: int
    teacher_name: Optional[str] = None
    session_date: date
    start_time: str
    end_time: str
    slot_name: Optional[str] = None
    is_confirmed: bool = False
    status: str = "SCHEDULED"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
