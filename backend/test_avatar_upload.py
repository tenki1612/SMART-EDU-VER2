import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_avatar_upload_flow():
    print("--- 1. Đăng nhập tài khoản kiểm thử ---")
    login_res = client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("--- 2. Kiểm tra upload file không phải ảnh (Phải bị từ chối 400) ---")
    fake_txt = io.BytesIO(b"Hello world this is not an image")
    bad_res = client.post(
        "/api/v1/accounts/me/avatar/upload",
        files={"file": ("malicious.txt", fake_txt, "text/plain")},
        headers=headers
    )
    assert bad_res.status_code == 400, f"Expected 400, got: {bad_res.status_code} - {bad_res.text}"
    print("=> Tuân thủ: File văn bản bị từ chối chính xác.")

    print("--- 3. Kiểm tra upload file ảnh hợp lệ (PNG) ---")
    # 1x1 PNG binary data
    png_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc`\x00\x00\x00'
        b'\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    img_file = io.BytesIO(png_bytes)
    upload_res = client.post(
        "/api/v1/accounts/me/avatar/upload",
        files={"file": ("test_avatar.png", img_file, "image/png")},
        headers=headers
    )
    assert upload_res.status_code == 200, f"Upload failed: {upload_res.status_code} - {upload_res.text}"
    data = upload_res.json()["data"]
    new_avatar_url = data["avatar_url"]
    print(f"=> Upload thành công! URL avatar mới: {new_avatar_url}")
    assert new_avatar_url.startswith("/uploads/avatars/"), f"Invalid avatar url: {new_avatar_url}"

    print("--- 4. Kiểm tra StaticFiles phục vụ ảnh đại diện ---")
    static_res = client.get(new_avatar_url)
    assert static_res.status_code == 200, f"Cannot get static avatar: {static_res.status_code}"
    assert len(static_res.content) == len(png_bytes)
    print("=> StaticFiles phục vụ ảnh đại diện chính xác 200 OK.")

    print("--- 5. Kiểm tra xóa ảnh đại diện (DELETE /me/avatar) ---")
    del_res = client.delete("/api/v1/accounts/me/avatar", headers=headers)
    assert del_res.status_code == 200, f"Delete avatar failed: {del_res.status_code}"
    del_data = del_res.json()["data"]
    assert del_data["avatar_url"] is None, "Avatar was not set to None"
    print("=> Xóa ảnh đại diện thành công!")

    print("\n>>> TẤT CẢ CÁC BƯỚC TEST AVATAR UPLOAD ĐÃ PASS 100%! <<<")

if __name__ == "__main__":
    test_avatar_upload_flow()
