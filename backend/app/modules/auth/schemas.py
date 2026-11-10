from typing import Optional
from pydantic import BaseModel, EmailStr
from app.core.permissions import RoleEnum

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str
    phone: Optional[str] = None
    role: RoleEnum = RoleEnum.STUDENT

class RegisterParentForStaffRequest(BaseModel):
    """
    Cho phép Admin, Staff, Teacher đăng ký thêm tài khoản Phụ huynh cho bản thân:
    - Giữ nguyên thông tin cá nhân (Họ tên) và số điện thoại
    - Username mới cho tài khoản phụ huynh (mặc định hoặc tự chọn)
    - Mật khẩu cho tài khoản phụ huynh (mặc định dùng chung mật khẩu hoặc đặt mới)
    - Liên kết tới học viên con em (nếu có student_id)
    """
    username: Optional[str] = None
    password: Optional[str] = None
    student_id: Optional[int] = None
    relationship_type: Optional[str] = "Phụ huynh / Người giám hộ"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    full_name: str
    role: RoleEnum
    avatar_url: Optional[str] = None

class UserInfoResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: RoleEnum
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True

class ForgotPasswordRequest(BaseModel):
    identifier: str

class ForgotPasswordResponse(BaseModel):
    identifier: str
    reset_code: str
    expires_in_minutes: int = 15
    message: str

class ResetPasswordRequest(BaseModel):
    identifier: str
    reset_code: str
    new_password: str

class ResetPasswordResponse(BaseModel):
    success: bool = True
    message: str
