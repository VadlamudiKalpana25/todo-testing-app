from fastapi.testclient import TestClient
from backend.main import app   # if your main.py is in backend folder; otherwise: from main import app

client = TestClient(app)

def test_register_success():
    payload = {"email": "unit_user01@test.com", "password": "Password@123"}
    r = client.post("/auth/register", json=payload)
    # Accept 201 OR 409 if already exists (rerun safe)
    assert r.status_code in (201, 409), r.text

def test_login_success():
    payload = {"email": "unit_user01@test.com", "password": "Password@123"}
    r = client.post("/auth/login-json", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "access_token" in data
    assert data.get("token_type") in ("bearer", "Bearer", None)
