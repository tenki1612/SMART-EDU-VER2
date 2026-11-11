import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token(username, password):
    res = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200, f"Login failed for {username}: {res.text}"
    return res.json()["data"]["access_token"]

def test_accounts_search_and_list():
    admin_token = get_token("admin", "admin123")
    res = client.get("/api/v1/accounts/", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    data = res.json()["data"]
    assert len(data) > 0

    # Filter by role
    staff_res = client.get("/api/v1/accounts/?role=TEACHER", headers={"Authorization": f"Bearer {admin_token}"})
    assert staff_res.status_code == 200
    for u in staff_res.json()["data"]:
        assert u["role"] == "TEACHER"

def test_accounts_staff_cannot_elevate_role():
    staff_token = get_token("staff", "staff123")
    # Staff tries to elevate role of student -> should be 403 Forbidden
    res = client.patch("/api/v1/accounts/1/role", 
        headers={"Authorization": f"Bearer {staff_token}"},
        json={"role": "ADMIN"}
    )
    assert res.status_code == 403

def test_accounts_staff_cannot_toggle_lock():
    staff_token = get_token("staff", "staff123")
    res = client.patch("/api/v1/accounts/1/toggle-lock", 
        headers={"Authorization": f"Bearer {staff_token}"}
    )
    assert res.status_code == 403

def test_create_and_elevate_and_lock_account():
    admin_token = get_token("admin", "admin123")
    uname = f"test_acc_{int(time.time())}"
    
    # 1. Tạo tài khoản mới thủ công
    create_res = client.post("/api/v1/accounts/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "username": uname,
            "email": f"{uname}@example.com",
            "full_name": "Test Account FR07",
            "password": "password123",
            "role": "STUDENT",
            "phone": "0988001122"
        }
    )
    assert create_res.status_code == 200
    user_id = create_res.json()["data"]["id"]
    assert create_res.json()["data"]["role"] == "STUDENT"

    # 2. Admin nâng quyền thành TEACHER (FR-08) -> tự động tạo mã giáo viên GVxxxx
    elevate_res = client.patch(f"/api/v1/accounts/{user_id}/role",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"role": "TEACHER"}
    )
    assert elevate_res.status_code == 200
    assert elevate_res.json()["data"]["role"] == "TEACHER"

    # Kiểm tra related-students / profile của Teacher vừa nâng
    rel_res = client.get(f"/api/v1/accounts/{user_id}/related-students",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert rel_res.status_code == 200
    assert len(rel_res.json()["data"]) > 0
    assert rel_res.json()["data"][0]["teacher_code"] == f"GV{user_id:04d}"

    # 3. Đăng nhập thử bằng tài khoản vừa tạo
    user_token = get_token(uname, "password123")
    assert user_token is not None

    # 4. Admin Khóa tài khoản (FR-09)
    lock_res = client.patch(f"/api/v1/accounts/{user_id}/toggle-lock",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert lock_res.status_code == 200
    assert lock_res.json()["data"]["is_active"] is False

    # 5. Đăng nhập khi bị khóa -> Bị từ chối
    blocked_login = client.post("/api/v1/auth/login", json={"username": uname, "password": "password123"})
    assert blocked_login.status_code == 400
    assert "bị Quản trị viên khóa" in blocked_login.json()["detail"]

    # 6. Mở khóa lại
    unlock_res = client.patch(f"/api/v1/accounts/{user_id}/toggle-lock",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert unlock_res.status_code == 200
    assert unlock_res.json()["data"]["is_active"] is True

    # 7. Admin Reset Password (FR-10)
    reset_res = client.post(f"/api/v1/accounts/{user_id}/reset-password",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"new_password": "new_admin_password_999"}
    )
    assert reset_res.status_code == 200

    # Đăng nhập bằng mật khẩu mới vừa được Admin reset
    new_login = client.post("/api/v1/auth/login", json={"username": uname, "password": "new_admin_password_999"})
    assert new_login.status_code == 200

    # 8. Xóa tài khoản (Soft delete)
    del_res = client.delete(f"/api/v1/accounts/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert del_res.status_code == 200

    print("🎉 ALL ACCOUNT TESTS PASSED 100%!")

if __name__ == "__main__":
    test_accounts_search_and_list()
    test_accounts_staff_cannot_elevate_role()
    test_accounts_staff_cannot_toggle_lock()
    test_create_and_elevate_and_lock_account()
