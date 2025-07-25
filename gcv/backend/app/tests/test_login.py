from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_test_login():
    response = client.get("/api/v1/login/test")
    assert response.status_code == 200
    assert response.json() == {"message": "test"}
