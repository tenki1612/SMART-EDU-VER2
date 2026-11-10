import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_login_dang_nhap_success():
    response = client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert data["data"]["role"] == "ADMIN"

def test_login_wrong_password():
    response = client.post("/api/v1/auth/login", json={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == 400
    assert "Mật khẩu không chính xác" in response.json()["detail"]

def test_get_me_with_token():
    login_res = client.post("/api/v1/auth/login", json={"username": "staff", "password": "staff123"})
    token = login_res.json()["data"]["access_token"]
    
    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["success"] is True
    assert me_data["data"]["username"] == "staff"
    assert me_data["data"]["role"] == "ACADEMIC_STAFF"

def test_doi_mat_khau():
    # Login teacher
    login_res = client.post("/api/v1/auth/login", json={"username": "teacher", "password": "teacher123"})
    token = login_res.json()["data"]["access_token"]
    
    # Change password
    chg_res = client.post("/api/v1/auth/change-password", 
        headers={"Authorization": f"Bearer {token}"},
        json={"old_password": "teacher123", "new_password": "teacher_new_456"}
    )
    assert chg_res.status_code == 200
    assert chg_res.json()["success"] is True

    # Test login with new password
    new_login = client.post("/api/v1/auth/login", json={"username": "teacher", "password": "teacher_new_456"})
    assert new_login.status_code == 200

    # Restore password back
    token2 = new_login.json()["data"]["access_token"]
    restore_res = client.post("/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {token2}"},
        json={"old_password": "teacher_new_456", "new_password": "teacher123"}
    )
    assert restore_res.status_code == 200

def test_dang_ky_tai_khoan_phu_huynh_cho_admin_staff_teacher():
    """Kiểm tra Admin/Staff/Teacher tự đăng ký thêm tài khoản Phụ huynh cho bản thân"""
    # 1. Staff đăng nhập
    staff_login = client.post("/api/v1/auth/login", json={"username": "staff", "password": "staff123"})
    assert staff_login.status_code == 200
    token = staff_login.json()["data"]["access_token"]
    
    # Lấy thông tin Staff hiện tại
    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}).json()["data"]
    staff_full_name = me["full_name"]
    staff_phone = me["phone"]
    
    # 2. Staff đăng ký thêm tài khoản Phụ huynh
    parent_res = client.post("/api/v1/auth/register-parent",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "staff_parent_test",
            "relationship_type": "Mẹ ruột"
        }
    )
    assert parent_res.status_code == 200
    parent_data = parent_res.json()["data"]
    assert parent_data["role"] == "PARENT"
    assert parent_data["full_name"] == staff_full_name
    
    # 3. Đăng nhập thử bằng tài khoản Phụ huynh vừa tạo
    # Mật khẩu kế thừa từ staff123
    parent_login = client.post("/api/v1/auth/login", json={"username": "staff_parent_test", "password": "staff123"})
    assert parent_login.status_code == 200
    parent_token = parent_login.json()["data"]["access_token"]
    
    # Lấy profile tài khoản phụ huynh để kiểm tra thông tin và số điện thoại giữ nguyên
    parent_profile = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {parent_token}"}).json()["data"]
    assert parent_profile["full_name"] == staff_full_name
    assert parent_profile["phone"] == staff_phone
    assert parent_profile["role"] == "PARENT"
    print("✅ Verified: Staff registered Parent account with identical full name and phone number!")

def test_forgot_and_reset_password_quen_mat_khau():
    forgot_res = client.post("/api/v1/auth/forgot-password", json={"identifier": "student"})
    assert forgot_res.status_code == 200
    otp = forgot_res.json()["data"]["reset_code"]
    assert len(otp) == 6

    reset_res = client.post("/api/v1/auth/reset-password", json={
        "identifier": "student",
        "reset_code": otp,
        "new_password": "student_new_123"
    })
    assert reset_res.status_code == 200

    new_login = client.post("/api/v1/auth/login", json={"username": "student", "password": "student_new_123"})
    assert new_login.status_code == 200

    # Restore
    forgot_res2 = client.post("/api/v1/auth/forgot-password", json={"identifier": "student"})
    otp2 = forgot_res2.json()["data"]["reset_code"]
    client.post("/api/v1/auth/reset-password", json={
        "identifier": "student",
        "reset_code": otp2,
        "new_password": "student123"
    })

if __name__ == "__main__":
    test_health_check()
    test_login_dang_nhap_success()
    test_login_wrong_password()
    test_get_me_with_token()
    test_doi_mat_khau()
    test_dang_ky_tai_khoan_phu_huynh_cho_admin_staff_teacher()
    test_forgot_and_reset_password_quen_mat_khau()
    print("🎉 ALL TESTS WITH CLASS DIAGRAM ALIGNMENT PASSED!")
