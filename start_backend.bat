@echo off
chcp 65001 >nul
echo ===================================================
echo 🚀 KHỞI ĐỘNG FASTAPI BACKEND - SMART-EDU LMS
echo ===================================================
cd /d "%~dp0backend"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
