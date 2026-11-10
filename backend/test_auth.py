import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_login_success():
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
    # Login first
    login_res = client.post("/api/v1/auth/login", json={"username": "staff", "password": "staff123"})
    token = login_res.json()["data"]["access_token"]
    
    # Get current user info
    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["success"] is True
    assert me_data["data"]["username"] == "staff"
    assert me_data["data"]["role"] == "ACADEMIC_STAFF"

def test_get_roles_permissions():
    login_res = client.post("/api/v1/auth/login", json={"username": "teacher", "password": "teacher123"})
    token = login_res.json()["data"]["access_token"]
    
    res = client.get("/api/v1/auth/roles-permissions", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert len(res.json()["data"]) == 5

def test_forgot_and_reset_password_flow():
    # 1. Request OTP
    forgot_res = client.post("/api/v1/auth/forgot-password", json={"identifier": "student"})
    assert forgot_res.status_code == 200
    otp = forgot_res.json()["data"]["reset_code"]
    assert len(otp) == 6

    # 2. Reset password with OTP
    reset_res = client.post("/api/v1/auth/reset-password", json={
        "identifier": "student",
        "reset_code": otp,
        "new_password": "student_new_123"
    })
    assert reset_res.status_code == 200
    assert reset_res.json()["data"]["success"] is True

    # 3. Login with new password
    new_login = client.post("/api/v1/auth/login", json={"username": "student", "password": "student_new_123"})
    assert new_login.status_code == 200

    # 4. Restore original password
    client.post("/api/v1/auth/forgot-password", json={"identifier": "student"})
    forgot_res2 = client.post("/api/v1/auth/forgot-password", json={"identifier": "student"})
    otp2 = forgot_res2.json()["data"]["reset_code"]
    client.post("/api/v1/auth/reset-password", json={
        "identifier": "student",
        "reset_code": otp2,
        "new_password": "student123"
    })
    # Verify restored
    restore_login = client.post("/api/v1/auth/login", json={"username": "student", "password": "student123"})
    assert restore_login.status_code == 200

def test_register_new_student():
    import time
    uname = f"testuser_{int(time.time())}"
    res = client.post("/api/v1/auth/register", json={
        "username": uname,
        "email": f"{uname}@example.com",
        "full_name": "Nguyen Van Test",
        "password": "password123",
        "phone": "0912345678",
        "role": "STUDENT"
    })
    assert res.status_code == 200
    assert res.json()["success"] is True
    assert res.json()["data"]["username"] == uname
    assert res.json()["data"]["role"] == "STUDENT"

if __name__ == "__main__":
    test_health_check()
    test_login_success()
    test_login_wrong_password()
    test_get_me_with_token()
    test_get_roles_permissions()
    test_forgot_and_reset_password_flow()
    test_register_new_student()
    print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
