from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_roles, RoleEnum, get_current_user_payload
from app.common.response import ApiResponse
from app.modules.courses.schemas import CourseCreate, CourseUpdate, CourseResponse
from app.modules.courses.service import CourseService

router = APIRouter()

# -------------------------------------------------------------
# 1. TRA CỨU KHÓA ĐÀO TẠO (Dành cho mọi người dùng)
# -------------------------------------------------------------
@router.get(
    "/",
    response_model=ApiResponse[List[CourseResponse]],
    summary="FR-11: Danh sách khóa đào tạo & biểu phí chuẩn"
)
def list_courses(
    q: Optional[str] = Query(None, description="Từ khóa tìm kiếm (tên, mã, chuẩn đầu ra)"),
    only_active: bool = Query(False, description="Chỉ lấy các khóa đang kích hoạt"),
    target_level: Optional[str] = Query(None, description="Lọc theo chuẩn đầu ra (IELTS, TOEIC...)"),
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    courses = CourseService.list_courses(db, q=q, only_active=only_active, target_level=target_level)
    return ApiResponse(data=courses, message="Lấy danh sách khóa học thành công")


@router.get(
    "/{id}",
    response_model=ApiResponse[CourseResponse],
    summary="FR-12: Chi tiết khóa đào tạo theo ID"
)
def get_course(
    id: int,
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    course = CourseService.get_by_id(db, course_id=id)
    return ApiResponse(data=course, message="Lấy chi tiết khóa học thành công")


# -------------------------------------------------------------
# 2. QUẢN TRỊ & THIẾT LẬP KHÓA HỌC (ADMIN & ACADEMIC_STAFF)
# -------------------------------------------------------------
@router.post(
    "/",
    response_model=ApiResponse[CourseResponse],
    summary="FR-13: Tạo khóa đào tạo mới",
    dependencies=[Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))]
)
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db)
):
    course = CourseService.create_course(db, data=data)
    return ApiResponse(data=course, message="Tạo khóa học mới thành công")


@router.put(
    "/{id}",
    response_model=ApiResponse[CourseResponse],
    summary="FR-14: Cập nhật thông tin khóa đào tạo",
    dependencies=[Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))]
)
def update_course(
    id: int,
    data: CourseUpdate,
    db: Session = Depends(get_db)
):
    course = CourseService.update_course(db, course_id=id, data=data)
    return ApiResponse(data=course, message="Cập nhật thông tin khóa học thành công")


@router.patch(
    "/{id}/toggle-status",
    response_model=ApiResponse[CourseResponse],
    summary="FR-15: Bật/tắt trạng thái kích hoạt khóa học",
    dependencies=[Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))]
)
def toggle_course_status(
    id: int,
    db: Session = Depends(get_db)
):
    course = CourseService.toggle_status(db, course_id=id)
    state = "Kích hoạt" if course.is_active else "Tạm ngưng"
    return ApiResponse(data=course, message=f"Đã chuyển trạng thái khóa học sang '{state}'")


@router.delete(
    "/{id}",
    response_model=ApiResponse[dict],
    summary="FR-16: Xóa khóa đào tạo (Soft delete)",
    dependencies=[Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))]
)
def delete_course(
    id: int,
    db: Session = Depends(get_db)
):
    CourseService.delete_course(db, course_id=id)
    return ApiResponse(data={"deleted_id": id}, message="Xóa khóa học thành công")
