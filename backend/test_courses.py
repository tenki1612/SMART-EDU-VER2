import shutil
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import get_db
from app.main import app

# Chạy test trên bản sao SQLite database độc lập
_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEV_DB = _REPO_ROOT / "database" / "language_center.db"
_TMP_DIR = tempfile.mkdtemp(prefix="smartech_courses_test_")
_TEST_DB = Path(_TMP_DIR) / "language_center_test.db"
if _DEV_DB.exists():
    shutil.copy(_DEV_DB, _TEST_DB)

_test_engine = create_engine(f"sqlite:///{_TEST_DB.as_posix()}", connect_args={"check_same_thread": False})
_TestSession = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)


def _override_get_db():
    db = _TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db
client = TestClient(app)


def get_token(username, password):
    res = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200, f"Login failed for {username}: {res.text}"
    return res.json()["data"]["access_token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# 1. TEST DANH SÁCH & TÌM KIẾM KHÓA HỌC (FR-11, FR-12)
# ---------------------------------------------------------------------------
def test_list_courses():
    token = get_token("staff", "staff123")
    res = client.get("/api/v1/courses/", headers=auth(token))
    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    assert len(body["data"]) > 0


def test_search_courses_by_keyword():
    token = get_token("student", "student123")
    res = client.get("/api/v1/courses/?q=IELTS", headers=auth(token))
    assert res.status_code == 200
    courses = res.json()["data"]
    assert len(courses) > 0
    for c in courses:
        assert (
            "IELTS" in c["code"].upper()
            or "IELTS" in c["title"].upper()
            or "IELTS" in c["target_level"].upper()
        )


def test_filter_active_courses():
    token = get_token("staff", "staff123")
    res = client.get("/api/v1/courses/?only_active=true", headers=auth(token))
    assert res.status_code == 200
    courses = res.json()["data"]
    for c in courses:
        assert c["is_active"] is True


def test_get_course_detail():
    token = get_token("staff", "staff123")
    res = client.get("/api/v1/courses/1", headers=auth(token))
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["id"] == 1
    assert "code" in data
    assert "fee" in data


def test_get_course_not_found():
    token = get_token("staff", "staff123")
    res = client.get("/api/v1/courses/99999", headers=auth(token))
    assert res.status_code == 404


# ---------------------------------------------------------------------------
# 2. TEST TẠO MỚI & RÀNG BUỘC NGHIỆP VỤ (FR-13)
# ---------------------------------------------------------------------------
def test_create_course_success():
    token = get_token("admin", "admin123")
    payload = {
        "code": "TEST-SAT-1400",
        "title": "Khóa Luyện Thi SAT Cấp Tốc 1400+",
        "description": "Chương trình ôn luyện kỹ năng Đọc hiểu và Toán chuyên sâu",
        "target_level": "SAT 1400+",
        "duration_weeks": 10,
        "fee": 9500000.0,
    }
    res = client.post("/api/v1/courses/", json=payload, headers=auth(token))
    assert res.status_code == 200
    created = res.json()["data"]
    assert created["code"] == "TEST-SAT-1400"
    assert created["fee"] == 9500000.0
    assert created["is_active"] is True


def test_create_duplicate_course_code_conflict():
    token = get_token("admin", "admin123")
    payload = {
        "code": "TEST-SAT-1400",  # Mã đã tạo ở test trước
        "title": "Khóa Trùng Mã",
        "target_level": "SAT 1400+",
        "duration_weeks": 10,
        "fee": 9500000.0,
    }
    res = client.post("/api/v1/courses/", json=payload, headers=auth(token))
    assert res.status_code == 409
    error_msg = res.json().get("detail") or res.json().get("message", "")
    assert "đã tồn tại" in error_msg


def test_create_course_invalid_duration_weeks():
    token = get_token("admin", "admin123")
    payload = {
        "code": "INVALID-WEEKS",
        "title": "Khóa Lỗi Tuần",
        "target_level": "A1",
        "duration_weeks": 0,  # Không hợp lệ
        "fee": 1000000.0,
    }
    res = client.post("/api/v1/courses/", json=payload, headers=auth(token))
    assert res.status_code in (400, 422)


def test_student_cannot_create_course():
    token = get_token("student", "student123")
    payload = {
        "code": "HACK-COURSE",
        "title": "Khóa Học Bất Hợp Pháp",
        "target_level": "Test",
        "duration_weeks": 5,
        "fee": 1000.0,
    }
    res = client.post("/api/v1/courses/", json=payload, headers=auth(token))
    assert res.status_code == 403


# ---------------------------------------------------------------------------
# 3. TEST CẬP NHẬT, CHUYỂN TRẠNG THÁI & XÓA KHÓA HỌC (FR-14, FR-15, FR-16)
# ---------------------------------------------------------------------------
def test_update_course():
    token = get_token("staff", "staff123")
    # Cập nhật khóa TEST-SAT-1400 vừa tạo
    find_res = client.get("/api/v1/courses/?q=TEST-SAT-1400", headers=auth(token))
    course_id = find_res.json()["data"][0]["id"]

    update_payload = {
        "title": "Khóa Luyện Thi SAT Cấp Tốc 1450+ (Updated)",
        "fee": 11000000.0,
        "duration_weeks": 12,
    }
    res = client.put(f"/api/v1/courses/{course_id}", json=update_payload, headers=auth(token))
    assert res.status_code == 200
    updated = res.json()["data"]
    assert updated["title"] == "Khóa Luyện Thi SAT Cấp Tốc 1450+ (Updated)"
    assert updated["fee"] == 11000000.0
    assert updated["duration_weeks"] == 12


def test_toggle_course_status():
    token = get_token("staff", "staff123")
    find_res = client.get("/api/v1/courses/?q=TEST-SAT-1400", headers=auth(token))
    course_id = find_res.json()["data"][0]["id"]
    current_status = find_res.json()["data"][0]["is_active"]

    res = client.patch(f"/api/v1/courses/{course_id}/toggle-status", headers=auth(token))
    assert res.status_code == 200
    assert res.json()["data"]["is_active"] == (not current_status)


def test_delete_course_with_active_classes_blocked():
    token = get_token("admin", "admin123")
    # Khóa ID = 1 (IELTS 6.5) đã có lớp học liên kết trong DB ban đầu
    res = client.delete("/api/v1/courses/1", headers=auth(token))
    assert res.status_code == 400
    error_msg = res.json().get("detail") or res.json().get("message", "")
    assert "lớp học liên kết" in error_msg


def test_delete_course_without_classes_success():
    token = get_token("admin", "admin123")
    # Khóa TEST-SAT-1400 không có lớp học liên kết -> được phép xóa mềm
    find_res = client.get("/api/v1/courses/?q=TEST-SAT-1400", headers=auth(token))
    course_id = find_res.json()["data"][0]["id"]

    res = client.delete(f"/api/v1/courses/{course_id}", headers=auth(token))
    assert res.status_code == 200
    assert res.json()["success"] is True

    # Không còn tìm thấy trong danh sách
    get_res = client.get(f"/api/v1/courses/{course_id}", headers=auth(token))
    assert get_res.status_code == 404
