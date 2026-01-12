from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def get_token():
    # ensure user exists
    client.post("/auth/register", json={"email":"unit_user02@test.com","password":"Password@123"})
    r = client.post("/auth/login-json", json={"email":"unit_user02@test.com","password":"Password@123"})
    return r.json()["access_token"]

def test_get_todos_unauthorized():
    r = client.get("/todos")
    assert r.status_code in (401, 403), r.text

def test_create_todo_authorized():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    r = client.post("/todos", json={"title":"Unit todo", "completed": False}, headers=headers)
    assert r.status_code in (200, 201), r.text
    data = r.json()
    assert "id" in data
    assert data["title"] == "Unit todo"
