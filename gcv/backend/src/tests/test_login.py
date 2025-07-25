from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.tests.utils.user import create_random_user, user_authentication_headers

client = TestClient(app)

def test_get_access_token(db) -> None:
    user = create_random_user(db)
    login_data = {
        "username": user.email,
        "password": "password",
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]

def test_use_access_token(db) -> None:
    user = create_random_user(db)
    headers = user_authentication_headers(client=client, email=user.email, password="password")
    r = client.post(f"{settings.API_V1_STR}/login/test-token", headers=headers)
    result = r.json()
    assert r.status_code == 200
    assert "email" in result
    assert result["email"] == user.email
