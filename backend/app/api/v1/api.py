from fastapi import APIRouter
from app.modules.auth.router import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["01. Đăng nhập & Phân quyền (FR-01 -> FR-06)"])
