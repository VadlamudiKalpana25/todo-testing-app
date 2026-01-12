import requests

BASE_URL = "http://127.0.0.1:8000"

def test_user_login():
    payload = {
        "email": "user02@test.com",
        "password": "Password@123"
    }

    response = requests.post(
        f"{BASE_URL}/auth/login-json",
        json=payload
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
