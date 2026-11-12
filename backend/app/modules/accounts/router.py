import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, File, UploadFile
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.core.permissions import require_roles, RoleEnum, get_current_user_payload
from app.core.exceptions import BusinessException, NotFoundException
from app.common.response import ApiResponse
from app.modules.accounts.models import User
from app.modules.accounts.schemas import (
    UserCreate, UserUpdate, UserResponse, ChangePasswordRequest, 
    RoleUpdateRequest, AdminResetPasswordRequest, AvatarUpdateRequest
)
from app.modules.accounts.service import AccountService

router = APIRouter()

# -------------------------------------------------------------
# 1. TẠO TÀI KHOẢN MỚI THỦ CÔNG
# -------------------------------------------------------------
@router.post("/", response_model=ApiResponse[UserResponse], summary="FR-07: Thêm tài khoản thủ công")
def create_account(
    data: UserCreate, 
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    user = AccountService.create_user(db, data)
    return ApiResponse(data=user, message="Tạo tài khoản thành công")

# -------------------------------------------------------------
# 2. XEM DANH SÁCH & TÌM KIẾM TÀI KHOẢN
# -------------------------------------------------------------
@router.get("/", response_model=ApiResponse[List[UserResponse]], summary="FR-07/FR-09: Tìm kiếm & xem danh sách tài khoản")
def search_accounts(
    q: Optional[str] = Query(None, description="Tìm kiếm theo tên, username, email"),
    role: Optional[str] = Query(None, description="Lọc theo role"),
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    users = AccountService.search_users(db, query=q, role=role)
    return ApiResponse(data=users, message="Danh sách tài khoản")

# -------------------------------------------------------------
# 3. THÔNG TIN CÁ NHÂN (ME PROFILE & AVATAR)
# -------------------------------------------------------------
@router.get("/me", response_model=ApiResponse[UserResponse], summary="Xem thông tin tài khoản cá nhân")
def get_my_account(
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    user_id = int(payload["sub"])
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    return ApiResponse(data=user, message="Thông tin tài khoản")

@router.put("/me", response_model=ApiResponse[UserResponse], summary="Cập nhật thông tin tài khoản cá nhân")
def update_my_profile(
    data: UserUpdate,
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    user_id = int(payload["sub"])
    data.is_active = None
    user = AccountService.update_user(db, user_id, data)
    return ApiResponse(data=user, message="Cập nhật hồ sơ cá nhân thành công")

@router.patch("/me/avatar", response_model=ApiResponse[UserResponse], summary="Đổi ảnh đại diện cá nhân (URL / Mẫu có sẵn)")
def update_my_avatar(
    data: AvatarUpdateRequest,
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    user_id = int(payload["sub"])
    user = AccountService.update_user_avatar(db, user_id, data.avatar_url)
    return ApiResponse(data=user, message="Cập nhật ảnh đại diện thành công")

@router.post("/me/avatar/upload", response_model=ApiResponse[UserResponse], summary="Tải lên ảnh đại diện từ máy tính cá nhân")
async def upload_my_avatar(
    file: UploadFile = File(...),
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    user_id = int(payload["sub"])
    
    # 1. Kiểm tra định dạng tệp hình ảnh
    ext = os.path.splitext(file.filename or "")[1].lower()
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    allowed_content_types = {"image/jpeg", "image/png", "image/webp", "image/gif"}
    
    if ext not in allowed_extensions or (file.content_type and file.content_type not in allowed_content_types):
        raise BusinessException("Định dạng tệp không hợp lệ! Vui lòng chỉ tải lên tệp hình ảnh (PNG, JPG, WEBP, GIF).")
    
    # 2. Đọc nội dung tệp và kiểm tra dung lượng (tối đa 5MB)
    max_file_size = 5 * 1024 * 1024
    content = await file.read()
    if len(content) > max_file_size:
        raise BusinessException("Kích thước tệp vượt quá giới hạn cho phép (tối đa 5MB)!")
    if len(content) == 0:
        raise BusinessException("Tệp tải lên không được để trống!")
    
    # 3. Chuẩn bị thư mục uploads/avatars
    upload_folder = settings.AVATARS_DIR
    upload_folder.mkdir(parents=True, exist_ok=True)
    
    # 4. Tạo tên tệp độc nhất tránh xung đột và chống tấn công Path Traversal
    filename = f"avatar_u{user_id}_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}{ext}"
    target_path = upload_folder / filename
    
    with open(target_path, "wb") as f:
        f.write(content)
        
    relative_url = f"/uploads/avatars/{filename}"
    
    # 5. Cập nhật vào CSDL và dọn dẹp file avatar cũ trên máy chủ nếu có
    user = AccountService.update_user_avatar_file(db, user_id, relative_url, upload_folder)
    return ApiResponse(data=user, message="Tải lên và cập nhật ảnh đại diện thành công")

@router.delete("/me/avatar", response_model=ApiResponse[UserResponse], summary="Xóa ảnh đại diện cá nhân")
def delete_my_avatar(
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    user_id = int(payload["sub"])
    upload_folder = settings.AVATARS_DIR
    user = AccountService.delete_user_avatar(db, user_id, upload_folder)
    return ApiResponse(data=user, message="Đã xóa ảnh đại diện thành công")

@router.post("/change-password", response_model=ApiResponse[bool], summary="Đổi mật khẩu tài khoản cá nhân")
def change_password(
    data: ChangePasswordRequest,
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db)
):
    user_id = int(payload["sub"])
    AccountService.change_password(db, user_id, data)
    return ApiResponse(data=True, message="Đổi mật khẩu thành công")

# -------------------------------------------------------------
# 4. QUẢN LÝ TÀI KHOẢN (ADMIN / STAFF)
# -------------------------------------------------------------
@router.get("/{user_id}", response_model=ApiResponse[UserResponse], summary="Xem chi tiết tài khoản")
def get_account_detail(
    user_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if not user:
        raise NotFoundException("Tài khoản", user_id)
    return ApiResponse(data=user, message="Chi tiết tài khoản")

@router.put("/{user_id}", response_model=ApiResponse[UserResponse], summary="Cập nhật tài khoản")
def update_account(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    user = AccountService.update_user(db, user_id, data)
    return ApiResponse(data=user, message="Cập nhật tài khoản thành công")

@router.patch("/{user_id}/role", response_model=ApiResponse[UserResponse], summary="FR-08: Nâng quyền / Thay đổi vai trò (Chỉ Admin)")
@router.put("/{user_id}/role", response_model=ApiResponse[UserResponse], summary="FR-08: Nâng quyền / Thay đổi vai trò (Alias PUT)")
def update_account_role(
    user_id: int,
    data: RoleUpdateRequest,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN])),
    db: Session = Depends(get_db)
):
    current_admin_id = int(payload["sub"])
    user = AccountService.update_user_role(db, user_id, data.role, current_admin_id)
    return ApiResponse(data=user, message=f"Đã nâng cấp vai trò người dùng thành '{data.role.value}' thành công")

@router.patch("/{user_id}/toggle-lock", response_model=ApiResponse[UserResponse], summary="FR-09: Khóa / Mở khóa tài khoản (Chỉ Admin)")
@router.post("/{user_id}/toggle-lock", response_model=ApiResponse[UserResponse], summary="FR-09: Khóa / Mở khóa tài khoản (Alias POST)")
def toggle_account_lock(
    user_id: int,
    payload: dict = Depends(require_roles([RoleEnum.ADMIN])),
    db: Session = Depends(get_db)
):
    current_admin_id = int(payload["sub"])
    user, msg = AccountService.toggle_user_lock(db, user_id, current_admin_id)
    return ApiResponse(data=user, message=msg)

@router.post("/{user_id}/reset-password", response_model=ApiResponse[bool], summary="FR-10: Quản trị viên đặt lại mật khẩu cho tài khoản")
def admin_reset_password(
    user_id: int,
    data: AdminResetPasswordRequest,
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN]))
):
    AccountService.admin_reset_password(db, user_id, data.new_password)
    return ApiResponse(data=True, message="Đã đặt lại mật khẩu tài khoản thành công")

@router.get("/{user_id}/related-students", response_model=ApiResponse[List[dict]], summary="Xem danh sách học sinh liên quan đến tài khoản")
def get_related_students(
    user_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    target_user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if not target_user:
        raise NotFoundException("Tài khoản", user_id)
    
    related = []
    if target_user.role == RoleEnum.PARENT:
        from app.modules.progression_parent.models import ParentStudent
        links = db.query(ParentStudent).filter(ParentStudent.parent_user_id == user_id).all()
        for l in links:
            st = l.student
            if st and not st.is_deleted:
                u = st.user
                related.append({
                    "student_id": st.id,
                    "student_code": st.student_code,
                    "full_name": u.full_name if u else st.student_code,
                    "email": u.email if u else "",
                    "relation": "Con em / Người được giám hộ",
                    "status": st.status
                })
    elif target_user.role == RoleEnum.TEACHER:
        from app.modules.teachers.models import Teacher
        teacher = db.query(Teacher).filter(Teacher.user_id == user_id, Teacher.is_deleted == False).first()
        if teacher:
            related.append({
                "teacher_id": teacher.id,
                "teacher_code": teacher.teacher_code,
                "specialty": teacher.specialty,
                "degree": teacher.degree,
                "status": teacher.status
            })
    elif target_user.role == RoleEnum.STUDENT:
        from app.modules.students.models import Student
        st = db.query(Student).filter(Student.user_id == user_id, Student.is_deleted == False).first()
        if st:
            related.append({
                "student_id": st.id,
                "student_code": st.student_code,
                "full_name": target_user.full_name,
                "email": target_user.email,
                "relation": "Học viên sở hữu tài khoản",
                "status": st.status
            })

    return ApiResponse(data=related, message="Danh sách học sinh liên quan")

@router.delete("/{user_id}", response_model=ApiResponse[bool], summary="Xóa tài khoản (Soft Delete)")
def delete_account(
    user_id: int,
    payload: dict = Depends(get_current_user_payload),
    db: Session = Depends(get_db),
    _ = Depends(require_roles([RoleEnum.ADMIN, RoleEnum.ACADEMIC_STAFF]))
):
    current_user_id = int(payload["sub"])
    AccountService.delete_user(db, user_id, current_user_id=current_user_id)
    return ApiResponse(data=True, message="Xóa tài khoản thành công")
