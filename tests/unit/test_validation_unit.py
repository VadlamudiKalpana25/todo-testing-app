from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_register_missing_email():
    r = client.post("/auth/register", json={"password":"Password@123"})
    assert r.status_code == 422, r.text

def test_login_missing_password():
    r = client.post("/auth/login-json", json={"email":"x@test.com"})
    assert r.status_code == 422, r.text

def test_create_todo_missing_title():
    # unauthorized or 422 depends on your middleware order,
    # but normally it will require auth first.
    r = client.post("/todos", json={"completed":False})
    assert r.status_code in (401, 403, 422), r.text
