import shutil
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import get_db
from app.main import app

# Chạy test trên BẢN SAO database để không sửa file dev `database/language_center.db`
_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEV_DB = _REPO_ROOT / "database" / "language_center.db"
_TMP_DIR = tempfile.mkdtemp(prefix="smartech_enroll_test_")
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


def pick_open_class(token):
    """Chọn lớp đang mở mà học viên chưa ghi danh và còn chỗ"""
    res = client.get("/api/v1/enrollments/open-classes",
                     headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200, res.text
    classes = res.json()["data"]
    candidates = [c for c in classes if not c["is_enrolled"] and not c["is_full"]]
    assert len(candidates) > 0, "Không còn lớp mở để kiểm thử"
    return candidates[0]


def test_open_classes_listed_for_student():
    token = get_token("student", "student123")
    res = client.get("/api/v1/enrollments/open-classes",
                     headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) > 0
    first = data[0]
    for field in ("class_code", "course_title", "target_level", "current_enrolled", "max_capacity", "is_full"):
        assert field in first


def test_my_requests_returns_only_own():
    token = get_token("student", "student123")
    res = client.get("/api/v1/enrollments/my-requests", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) > 0
    for r in data:
        assert "student_name" in r and "class_code" in r and "status" in r


def test_student_cannot_list_all_requests():
    token = get_token("student", "student123")
    res = client.get("/api/v1/enrollments/requests", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403


def test_staff_lists_all_requests():
    token = get_token("staff", "staff123")
    res = client.get("/api/v1/enrollments/requests", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert len(res.json()["data"]) > 0


def test_full_enrollment_lifecycle():
    """Học viên gửi đơn -> Học vụ duyệt -> ghi danh & tăng sĩ số -> học viên không tự hủy được"""
    student_token = get_token("student", "student123")
    staff_token = get_token("staff", "staff123")

    cls = pick_open_class(student_token)
    class_id = cls["id"]
    enrolled_before = cls["current_enrolled"]

    # 1. Học viên gửi đơn đăng ký
    create_res = client.post("/api/v1/enrollments/", headers={"Authorization": f"Bearer {student_token}"},
                             json={"class_id": class_id, "note": "Kiểm thử vòng đời đăng ký FR-50"})
    assert create_res.status_code == 200, create_res.text
    request_id = create_res.json()["data"]["id"]
    assert create_res.json()["data"]["status"] == "PENDING"

    # 2. Chặn đơn trùng (1 học viên chỉ có 1 đơn PENDING cho 1 lớp)
    dup_res = client.post("/api/v1/enrollments/", headers={"Authorization": f"Bearer {student_token}"},
                          json={"class_id": class_id, "note": "Đơn trùng"})
    assert dup_res.status_code == 409
    assert "đơn đăng ký đang chờ duyệt" in dup_res.json()["detail"]

    # 3. Học vụ duyệt đơn -> ghi danh vào lớp & tăng current_enrolled
    approve_res = client.patch(f"/api/v1/enrollments/{request_id}/approve",
                               headers={"Authorization": f"Bearer {staff_token}"})
    assert approve_res.status_code == 200, approve_res.text
    assert approve_res.json()["data"]["status"] == "APPROVED"

    cls_after = client.get("/api/v1/enrollments/open-classes",
                           headers={"Authorization": f"Bearer {student_token}"}).json()["data"]
    updated = next(c for c in cls_after if c["id"] == class_id)
    assert updated["current_enrolled"] == enrolled_before + 1
    assert updated["is_enrolled"] is True

    # 4. Đơn đã duyệt -> học viên KHÔNG được tự hủy
    cancel_res = client.patch(f"/api/v1/enrollments/{request_id}/cancel",
                              headers={"Authorization": f"Bearer {student_token}"})
    assert cancel_res.status_code == 400
    assert "phê duyệt" in cancel_res.json()["detail"].lower()

    # 5. Duyệt lại đơn đã xử lý -> bị chặn
    re_approve = client.patch(f"/api/v1/enrollments/{request_id}/approve",
                              headers={"Authorization": f"Bearer {staff_token}"})
    assert re_approve.status_code == 400


def test_reject_requires_reason():
    student_token = get_token("student", "student123")
    staff_token = get_token("staff", "staff123")

    cls = pick_open_class(student_token)
    create_res = client.post("/api/v1/enrollments/", headers={"Authorization": f"Bearer {student_token}"},
                             json={"class_id": cls["id"], "note": "Kiểm thử từ chối FR-56"})
    request_id = create_res.json()["data"]["id"]

    # Từ chối thiếu lý do -> 422 do validation Pydantic
    missing = client.patch(f"/api/v1/enrollments/{request_id}/reject",
                            headers={"Authorization": f"Bearer {staff_token}"}, json={})
    assert missing.status_code == 422

    # Lý do rỗng -> bị chặn ở tầng service
    blank = client.patch(f"/api/v1/enrollments/{request_id}/reject",
                         headers={"Authorization": f"Bearer {staff_token}"}, json={"rejection_reason": "   "})
    assert blank.status_code == 400

    # Từ chối hợp lệ
    ok = client.patch(f"/api/v1/enrollments/{request_id}/reject",
                      headers={"Authorization": f"Bearer {staff_token}"},
                      json={"rejection_reason": "Lớp đã đủ sĩ số"})
    assert ok.status_code == 200
    assert ok.json()["data"]["status"] == "REJECTED"
    assert ok.json()["data"]["rejection_reason"] == "Lớp đã đủ sĩ số"


def test_student_cancels_pending_request():
    student_token = get_token("student", "student123")
    cls = pick_open_class(student_token)
    create_res = client.post("/api/v1/enrollments/", headers={"Authorization": f"Bearer {student_token}"},
                             json={"class_id": cls["id"], "note": "Kiểm thử hủy đơn FR-53"})
    request_id = create_res.json()["data"]["id"]

    cancel_res = client.patch(f"/api/v1/enrollments/{request_id}/cancel",
                              headers={"Authorization": f"Bearer {student_token}"})
    assert cancel_res.status_code == 200
    assert cancel_res.json()["data"]["status"] == "CANCELLED"


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
