from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_roles, RoleEnum, get_current_user_payload
from app.common.response import ApiResponse
from app.modules.schedules.schemas import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse,
    ConflictCheck,
    ConflictCheckResponse,
)
from app.modules.schedules.service import ScheduleService
from app.modules.schedules.reference_data import ReferenceDataService

router = APIRouter()

# -------------------------------------------------------------
# 1. XEM THỜI KHÓA BIỂU
# -------------------------------------------------------------
@router.get("/", response_model=ApiResponse[List[ScheduleResponse]], summary="FR-61: Lấy toàn bộ lịch học")
def list_schedules(
    class_id: Optional[int] = Query(None, description="Lọc theo lớp học"),
    teacher_id: Optional[int] = Query(None, description="Lọc theo giáo viên"),
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    sessions = ScheduleService.list_sessions(db, class_id=class_id, teacher_id=teacher_id)
    return ApiResponse(data=sessions, message="Danh sách buổi học trong thời khóa biểu")


@router.get("/personal", response_model=ApiResponse[List[ScheduleResponse]], summary="FR-63: Lịch học cá nhân (Giáo viên / Học viên)")
def list_personal_schedules(
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    user_id = int(payload["sub"])
    role = payload.get("role")
    sessions = ScheduleService.list_personal_sessions(db, user_id, role)
    return ApiResponse(data=sessions, message="Thời khóa biểu cá nhân")


@router.get("/reference-data", response_model=ApiResponse[dict], summary="Dữ liệu tham chiếu cho form xếp lịch")
def get_reference_data(
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    data = ReferenceDataService.get_all(db)
    return ApiResponse(data=data, message="Dữ liệu tham chiếu phòng học, giáo viên, lớp học và khóa học")


# -------------------------------------------------------------
# 2. THUẬT TOÁN PHÁT HIỆN XUNG ĐỘT
# -------------------------------------------------------------
@router.post("/check-conflicts", response_model=ApiResponse[ConflictCheckResponse], summary="FR-65: Kiểm tra xung đột lịch trước khi lưu")
@router.post("/check-conflict", response_model=ApiResponse[ConflictCheckResponse], summary="FR-65: Kiểm tra xung đột (Alias)")
def check_conflicts(
    data: ConflictCheck,
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    result = ScheduleService.check_conflict(db, data)
    return ApiResponse(data=result, message=result["message"])


# -------------------------------------------------------------
# 3. TẠO / CẬP NHẬT / HỦY / XÓA
# -------------------------------------------------------------
@router.post("/", response_model=ApiResponse[ScheduleResponse], summary="FR-62: Tạo buổi học mới (tự kiểm tra xung đột)")
def create_schedule(
    data: ScheduleCreate,
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    session = ScheduleService.create_session(db, data)
    return ApiResponse(data=session, message="Đã thêm buổi học vào thời khóa biểu")


@router.put("/{session_id}", response_model=ApiResponse[ScheduleResponse], summary="FR-64: Điều chỉnh buổi học")
def update_schedule(
    session_id: int,
    data: ScheduleUpdate,
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    session = ScheduleService.update_session(db, session_id, data)
    return ApiResponse(data=session, message="Cập nhật buổi học thành công")


@router.patch("/{session_id}/cancel", response_model=ApiResponse[ScheduleResponse], summary="FR-66: Hủy buổi học")
def cancel_schedule(
    session_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    session = ScheduleService.cancel_session(db, session_id)
    return ApiResponse(data=session, message="Đã hủy buổi học")


@router.delete("/{session_id}", response_model=ApiResponse[bool], summary="FR-67: Xóa buổi học")
def delete_schedule(
    session_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    ScheduleService.delete_session(db, session_id)
    return ApiResponse(data=True, message="Xóa buổi học thành công")


@router.patch("/classes/{class_id}/confirm", response_model=ApiResponse[dict], summary="FR-68: Xác nhận thời khóa biểu chính thức của lớp")
def confirm_class_schedule(
    class_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    result = ScheduleService.confirm_class_schedule(db, class_id)
    return ApiResponse(data=result, message=result["message"])
