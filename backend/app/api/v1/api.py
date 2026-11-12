from fastapi import APIRouter
from app.modules.auth.router import router as auth_router
from app.modules.accounts.router import router as accounts_router
from app.modules.enrollments.router import router as enrollments_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["01. Đăng nhập & Phân quyền (FR-01 -> FR-06)"])
api_router.include_router(accounts_router, prefix="/accounts", tags=["02. Quản trị Tài khoản (FR-07 -> FR-10)"])
api_router.include_router(enrollments_router, prefix="/enrollments", tags=["08. Đăng ký lớp học & Xét duyệt (FR-50 -> FR-60)"])
