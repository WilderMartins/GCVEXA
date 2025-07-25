from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .. import crud
from ..core.config import settings

def test_create_user(client: TestClient, db: Session):
    response = client.post(
        f"/api/v1/users/",
        json={"email": "test@example.com", "password": "testpassword", "full_name": "Test User"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

    user = crud.user.get_user_by_email(db, email="test@example.com")
    assert user
    # O primeiro usuário deve ser um admin
    assert user.roles[0].name == "Admin"

def test_login(client: TestClient, db: Session):
    # Primeiro, crie um usuário para poder fazer login
    client.post(
        f"/api/v1/users/",
        json={"email": "login@example.com", "password": "testpassword", "full_name": "Login User"},
    )

    # Tentar fazer login
    login_data = {"username": "login@example.com", "password": "testpassword"}
    response = client.post(f"/api/v1/login/access-token", data=login_data)

    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"

def test_login_wrong_password(client: TestClient, db: Session):
    client.post(
        f"/api/v1/users/",
        json={"email": "wrongpass@example.com", "password": "testpassword", "full_name": "Wrong Pass User"},
    )

    login_data = {"username": "wrongpass@example.com", "password": "wrongpassword"}
    response = client.post(f"/api/v1/login/access-token", data=login_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"

def test_protected_route_no_token(client: TestClient):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401 # ou 403 dependendo da implementação exata

def test_get_current_user(client: TestClient, db: Session):
    client.post(
        f"/api/v1/users/",
        json={"email": "me@example.com", "password": "testpassword", "full_name": "Me User"},
    )
    login_data = {"username": "me@example.com", "password": "testpassword"}
    login_response = client.post(f"/api/v1/login/access-token", data=login_data)
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/users/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
