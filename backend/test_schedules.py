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
_TMP_DIR = tempfile.mkdtemp(prefix="smartech_schedule_test_")
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


def test_staff_lists_all_sessions():
    token = get_token("staff", "staff123")
    res = client.get("/api/v1/schedules/", headers=auth(token))
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) > 0
    for field in ("class_code", "room_code", "teacher_name", "session_date", "start_time", "end_time", "is_confirmed"):
        assert field in data[0]


def test_student_cannot_list_all_sessions():
    token = get_token("student", "student123")
    res = client.get("/api/v1/schedules/", headers=auth(token))
    assert res.status_code == 403


def test_personal_schedule_for_teacher():
    token = get_token("teacher", "teacher123")
    res = client.get("/api/v1/schedules/personal", headers=auth(token))
    assert res.status_code == 200
    assert len(res.json()["data"]) > 0


def test_personal_schedule_for_student():
    token = get_token("student", "student123")
    res = client.get("/api/v1/schedules/personal", headers=auth(token))
    assert res.status_code == 200
    assert isinstance(res.json()["data"], list)


def test_classroom_conflict_is_detected():
    """KI-01: cùng phòng + cùng khung giờ + cùng ngày => xung đột"""
    staff = get_token("staff", "staff123")
    existing = client.get("/api/v1/schedules/", headers=auth(staff)).json()["data"][0]

    res = client.post("/api/v1/schedules/check-conflicts", headers=auth(staff), json={
        "classroom_id": existing["classroom_id"],
        "teacher_id": existing["teacher_id"],
        "session_date": existing["session_date"],
        "start_time": existing["start_time"],
        "end_time": existing["end_time"],
    })
    assert res.status_code == 200
    body = res.json()["data"]
    assert body["has_conflict"] is True
    assert body["conflict_type"] == "CLASSROOM"
    assert len(body["conflicts"]) > 0
    assert body["conflicts"][0]["room_code"] == existing["room_code"]
    assert body["conflicts"][0]["class_code"] == existing["class_code"]
    assert "Phòng học" in body["message"]


def test_teacher_conflict_is_detected():
    """KI-01: cùng giáo viên + khung giờ chồng lấn (khác phòng) => xung đột"""
    staff = get_token("staff", "staff123")
    existing = client.get("/api/v1/schedules/", headers=auth(staff)).json()["data"][0]

    # Phòng khác, nhưng trùng giáo viên + cùng ngày + cùng khung giờ
    other_room = 4 if existing["classroom_id"] != 4 else 7
    res = client.post("/api/v1/schedules/check-conflicts", headers=auth(staff), json={
        "classroom_id": other_room,
        "teacher_id": existing["teacher_id"],
        "session_date": existing["session_date"],
        "start_time": existing["start_time"],
        "end_time": existing["end_time"],
    })
    assert res.status_code == 200
    body = res.json()["data"]
    assert body["has_conflict"] is True
    assert body["conflict_type"] == "TEACHER"
    assert "Giáo viên" in body["message"]


def test_adjacent_sessions_do_not_conflict():
    """KI-01 edge case: ca 1 kết thúc 18:00, ca 2 bắt đầu 18:00 => hợp lệ"""
    staff = get_token("staff", "staff123")
    existing = client.get("/api/v1/schedules/", headers=auth(staff)).json()["data"][0]

    other_room = 4 if existing["classroom_id"] != 4 else 7
    res = client.post("/api/v1/schedules/check-conflicts", headers=auth(staff), json={
        "classroom_id": other_room,
        "teacher_id": existing["teacher_id"] + 999,
        "session_date": existing["session_date"],
        "start_time": existing["end_time"],
        "end_time": "22:00",
    })
    assert res.status_code == 200
    assert res.json()["data"]["has_conflict"] is False


def test_create_session_and_conflict_blocks_save():
    staff = get_token("staff", "staff123")
    existing = client.get("/api/v1/schedules/", headers=auth(staff)).json()["data"][0]

    # 1. Tạo buổi học hợp lệ (ngày chưa có lịch nào)
    create_res = client.post("/api/v1/schedules/", headers=auth(staff), json={
        "class_id": existing["class_id"],
        "classroom_id": existing["classroom_id"],
        "teacher_id": existing["teacher_id"],
        "session_date": "2026-12-20",
        "start_time": "08:00",
        "end_time": "10:00",
        "slot_name": "Ca sáng kiểm thử",
    })
    assert create_res.status_code == 200, create_res.text
    session_id = create_res.json()["data"]["id"]
    assert create_res.json()["data"]["is_confirmed"] is False

    # 2. Tạo buổi thứ 2 trùng phòng + trùng giáo viên + trùng giờ => bị chặn
    conflict_res = client.post("/api/v1/schedules/", headers=auth(staff), json={
        "class_id": existing["class_id"],
        "classroom_id": existing["classroom_id"],
        "teacher_id": existing["teacher_id"],
        "session_date": "2026-12-20",
        "start_time": "09:00",
        "end_time": "11:00",
    })
    assert conflict_res.status_code == 400
    assert "xung đột" in conflict_res.json()["detail"].lower()

    # 3. Cập nhật chính nó (exclude_session_id) thì không tự xung đột
    update_res = client.put(f"/api/v1/schedules/{session_id}", headers=auth(staff), json={
        "start_time": "08:30",
        "end_time": "10:30",
    })
    assert update_res.status_code == 200, update_res.text
    assert update_res.json()["data"]["start_time"] == "08:30"

    # 4. Hủy buổi học
    cancel_res = client.patch(f"/api/v1/schedules/{session_id}/cancel", headers=auth(staff))
    assert cancel_res.status_code == 200
    assert cancel_res.json()["data"]["status"] == "CANCELLED"

    # 5. Xóa buổi học
    delete_res = client.delete(f"/api/v1/schedules/{session_id}", headers=auth(staff))
    assert delete_res.status_code == 200


def test_confirm_class_schedule():
    staff = get_token("staff", "staff123")
    existing = client.get("/api/v1/schedules/", headers=auth(staff)).json()["data"][0]
    res = client.patch(f"/api/v1/schedules/classes/{existing['class_id']}/confirm", headers=auth(staff))
    assert res.status_code == 200, res.text
    assert res.json()["data"]["confirmed_count"] > 0


def test_reference_data_for_schedule_form():
    staff = get_token("staff", "staff123")
    res = client.get("/api/v1/schedules/reference-data", headers=auth(staff))
    assert res.status_code == 200
    data = res.json()["data"]
    for key in ("classrooms", "teachers", "classes", "courses"):
        assert key in data
        assert len(data[key]) > 0
    assert "room_code" in data["classrooms"][0]
    assert "full_name" in data["teachers"][0]
    assert "class_code" in data["classes"][0]
    assert "title" in data["courses"][0]
    # Phòng bảo trì không được xuất hiện trong danh sách chọn
    assert all(r["status"] != "MAINTENANCE" for r in data["classrooms"])


def test_maintenance_classroom_is_rejected():
    """Phòng học ở trạng thái MAINTENANCE bị từ chối khi xếp lịch"""
    staff = get_token("staff", "staff123")
    res = client.post("/api/v1/schedules/", headers=auth(staff), json={
        "class_id": 1,
        "classroom_id": 11,  # P.402 - MAINTENANCE
        "teacher_id": 1,
        "session_date": "2026-12-25",
        "start_time": "08:00",
        "end_time": "10:00",
    })
    assert res.status_code == 400
    assert "bảo trì" in res.json()["detail"].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
