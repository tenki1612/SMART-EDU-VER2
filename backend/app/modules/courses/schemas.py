from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CourseBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150, description="Tên khóa học")
    description: Optional[str] = Field(None, description="Mô tả chi tiết nội dung khóa học")
    target_level: str = Field(..., min_length=1, max_length=100, description="Chuẩn đầu ra (ví dụ: IELTS 6.5, TOEIC 750, B2 CEFR)")
    duration_weeks: int = Field(12, ge=1, le=104, description="Thời lượng khóa học (số tuần, 1-104)")
    fee: float = Field(0.0, ge=0.0, description="Mức học phí chuẩn (VNĐ)")


class CourseCreate(CourseBase):
    code: str = Field(..., min_length=2, max_length=50, description="Mã định danh duy nhất (ví dụ: IELTS-PREP-65)")


class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=150, description="Tên khóa học")
    description: Optional[str] = Field(None, description="Mô tả chi tiết nội dung khóa học")
    target_level: Optional[str] = Field(None, min_length=1, max_length=100, description="Chuẩn đầu ra")
    duration_weeks: Optional[int] = Field(None, ge=1, le=104, description="Thời lượng khóa học (số tuần)")
    fee: Optional[float] = Field(None, ge=0.0, description="Mức học phí chuẩn (VNĐ)")
    is_active: Optional[bool] = Field(None, description="Trạng thái kích hoạt")


class CourseResponse(BaseModel):
    id: int
    code: str
    title: str
    description: Optional[str] = None
    target_level: str
    duration_weeks: int
    fee: float
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
