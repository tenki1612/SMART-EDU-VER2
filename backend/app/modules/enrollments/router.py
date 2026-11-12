from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_roles, RoleEnum, get_current_user_payload
from app.common.response import ApiResponse
from app.modules.enrollments.schemas import (
    EnrollmentCreate,
    EnrollmentReject,
    EnrollmentRequestResponse,
)
from app.modules.enrollments.service import EnrollmentService

router = APIRouter()

# -------------------------------------------------------------
# 1. HỌC VIÊN: XEM LỚP MỞ ĐĂNG KÝ & GỬI ĐƠN
# -------------------------------------------------------------
@router.get("/open-classes", response_model=ApiResponse[List[dict]], summary="FR-50: Danh sách lớp đang mở tuyển sinh")
def list_open_classes(
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    user_id = int(payload["sub"])
    classes = EnrollmentService.list_open_classes(db, user_id)
    return ApiResponse(data=classes, message="Danh sách lớp học đang mở đăng ký")


@router.post("/", response_model=ApiResponse[EnrollmentRequestResponse], summary="FR-51: Học viên gửi đơn đăng ký lớp học")
@router.post("/register", response_model=ApiResponse[EnrollmentRequestResponse], summary="FR-51: Gửi đơn đăng ký (Alias)")
def create_enrollment_request(
    data: EnrollmentCreate,
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    user_id = int(payload["sub"])
    request = EnrollmentService.create_request(db, user_id, data)
    return ApiResponse(data=request, message="Đã gửi yêu cầu đăng ký lớp học, vui lòng chờ Học vụ xét duyệt")


@router.get("/my-requests", response_model=ApiResponse[List[EnrollmentRequestResponse]], summary="FR-52: Học viên xem các đơn đăng ký của mình")
def list_my_requests(
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    user_id = int(payload["sub"])
    requests = EnrollmentService.list_my_requests(db, user_id)
    return ApiResponse(data=requests, message="Danh sách đơn đăng ký của tôi")


@router.patch("/{request_id}/cancel", response_model=ApiResponse[EnrollmentRequestResponse], summary="FR-53: Học viên tự hủy đơn (chỉ khi PENDING)")
@router.post("/requests/{request_id}/cancel", response_model=ApiResponse[EnrollmentRequestResponse], summary="FR-53: Hủy đơn (Alias)")
def cancel_enrollment_request(
    request_id: int,
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    user_id = int(payload["sub"])
    request = EnrollmentService.cancel_request(db, request_id, user_id)
    return ApiResponse(data=request, message="Đã hủy yêu cầu đăng ký lớp học thành công")


# -------------------------------------------------------------
# 2. HỌC VỤ / ADMIN: XÉT DUYỆT ĐƠN
# -------------------------------------------------------------
@router.get("/requests", response_model=ApiResponse[List[EnrollmentRequestResponse]], summary="FR-54: Học vụ xem toàn bộ đơn đăng ký")
def list_all_requests(
    status: Optional[str] = Query(None, description="Lọc theo trạng thái: PENDING, APPROVED, REJECTED, CANCELLED"),
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    requests = EnrollmentService.list_all_requests(db, status)
    return ApiResponse(data=requests, message="Danh sách đơn đăng ký lớp học")


@router.get("/", response_model=ApiResponse[List[EnrollmentRequestResponse]], summary="FR-54: Danh sách đơn đăng ký (Alias)")
def list_requests_for_staff(
    status: Optional[str] = Query(None, description="Lọc theo trạng thái: PENDING, APPROVED, REJECTED, CANCELLED"),
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    requests = EnrollmentService.list_all_requests(db, status)
    return ApiResponse(data=requests, message="Danh sách đơn đăng ký lớp học")


@router.patch("/{request_id}/approve", response_model=ApiResponse[EnrollmentRequestResponse], summary="FR-55: Phê duyệt đơn đăng ký")
@router.post("/requests/{request_id}/approve", response_model=ApiResponse[EnrollmentRequestResponse], summary="FR-55: Phê duyệt đơn (Alias)")
def approve_enrollment_request(
    request_id: int,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF])),
    db: Session = Depends(get_db)
):
    reviewer_user_id = int(payload["sub"])
    request = EnrollmentService.approve_request(db, request_id, reviewer_user_id)
    return ApiResponse(data=request, message="Đã phê duyệt đơn và ghi danh học viên vào lớp học")


@router.patch("/{request_id}/reject", response_model=ApiResponse[EnrollmentRequestResponse], summary="FR-56: Từ chối đơn đăng ký kèm lý do")
@router.post("/requests/{request_id}/reject", response_model=ApiResponse[EnrollmentRequestResponse], summary="FR-56: Từ chối đơn (Alias)")
def reject_enrollment_request(
    request_id: int,
    data: EnrollmentReject,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF])),
    db: Session = Depends(get_db)
):
    reviewer_user_id = int(payload["sub"])
    request = EnrollmentService.reject_request(db, request_id, reviewer_user_id, data)
    return ApiResponse(data=request, message="Đã từ chối đơn đăng ký và gửi phản hồi tới học viên")
