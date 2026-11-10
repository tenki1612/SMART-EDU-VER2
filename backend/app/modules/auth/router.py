from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.permissions import get_current_user_payload, require_roles, RoleEnum
from app.common.response import ApiResponse
from app.modules.accounts.models import User
from app.modules.auth.schemas import (
    LoginRequest, RegisterRequest, TokenResponse, UserInfoResponse,
    ForgotPasswordRequest, ForgotPasswordResponse,
    ResetPasswordRequest, ResetPasswordResponse,
    RegisterParentForStaffRequest
)
from app.modules.auth.service import AuthService

router = APIRouter()

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

@router.post("/login", response_model=ApiResponse[TokenResponse], summary="FR-01: Đăng nhập (dangNhap)")
def login(creds: LoginRequest, db: Session = Depends(get_db)):
    result = AuthService.dang_nhap(db, creds)
    return ApiResponse(data=result, message="Đăng nhập thành công")

@router.post("/register", response_model=ApiResponse[TokenResponse], summary="Đăng ký tài khoản mới")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    result = AuthService.register_user(db, req)
    return ApiResponse(data=result, message="Đăng ký tài khoản thành công")

@router.post("/register-parent", response_model=ApiResponse[TokenResponse], summary="Admin, Staff, Teacher đăng ký thêm tài khoản Phụ huynh cho bản thân")
def register_parent(
    req: RegisterParentForStaffRequest,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF, RoleEnum.TEACHER])),
    db: Session = Depends(get_db)
):
    """
    Cho phép Admin, Academic Staff và Teacher tự đăng ký thêm 1 tài khoản Phụ huynh (PARENT) cho bản thân mình.
    Giữ nguyên thông tin cá nhân (Họ tên) và Số điện thoại liên lạc ban đầu.
    """
    user_id = int(payload["sub"])
    result = AuthService.register_parent_account_for_staff(db, user_id, req)
    return ApiResponse(data=result, message="Đăng ký tài khoản phụ huynh thành công (giữ nguyên thông tin và số điện thoại)")

@router.post("/change-password", response_model=ApiResponse[dict], summary="Đổi mật khẩu (doiMatKhau)")
def change_password(
    req: ChangePasswordRequest,
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    user_id = int(payload["sub"])
    AuthService.doi_mat_khau(db, user_id, req.old_password, req.new_password)
    return ApiResponse(data={"success": True}, message="Đổi mật khẩu thành công")

@router.post("/logout", response_model=ApiResponse[dict], summary="FR-02: Đăng xuất (dangXuat)")
def logout(payload: dict = Depends(get_current_user_payload)):
    user_id = int(payload["sub"])
    result = AuthService.dang_xuat(user_id)
    return ApiResponse(data=result, message="Đăng xuất khỏi hệ thống thành công")

@router.get("/me", response_model=ApiResponse[UserInfoResponse], summary="FR-04: Lấy thông tin phiên đăng nhập & quyền")
def get_me(payload: dict = Depends(get_current_user_payload), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    return ApiResponse(data=user, message="Lấy thông tin người dùng thành công")

@router.get("/roles-permissions", response_model=ApiResponse[list], summary="FR-03: Danh mục vai trò và ma trận phân quyền")
def get_roles_permissions(payload: dict = Depends(get_current_user_payload)):
    matrix = [
        {"role": "ADMIN", "description": "Toàn quyền quản trị hệ thống, tài khoản, khóa học, phòng học, lớp học"},
        {"role": "ACADEMIC_STAFF", "description": "Quản lý tuyển sinh, duyệt đăng ký, sắp xếp thời khóa biểu, xác nhận điểm, xét duyệt học tiếp"},
        {"role": "TEACHER", "description": "Xem lịch dạy, xem danh sách lớp, nhập và cập nhật điểm số học viên"},
        {"role": "STUDENT", "description": "Xem khóa học, đăng ký lớp, xem thời khóa biểu cá nhân, tra cứu điểm và kết quả"},
        {"role": "PARENT", "description": "Xem thông tin học viên được giám hộ, theo dõi thời khóa biểu và kết quả học tập của con"}
    ]
    return ApiResponse(data=matrix, message="Danh sách phân quyền theo vai trò")

@router.post("/forgot-password", response_model=ApiResponse[ForgotPasswordResponse], summary="Yêu cầu mã khôi phục mật khẩu OTP (quenMatKhau)")
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    res = AuthService.quen_mat_khau(db, req)
    return ApiResponse(data=res, message=res.message)

@router.post("/reset-password", response_model=ApiResponse[ResetPasswordResponse], summary="Đặt lại mật khẩu với mã OTP")
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    res = AuthService.reset_password(db, req)
    return ApiResponse(data=res, message=res.message)
