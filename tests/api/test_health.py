import requests

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
