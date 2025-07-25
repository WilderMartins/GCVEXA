from fastapi.testclient import TestClient
from app import crud, schemas
from app.core.config import settings
from app.db.session import SessionLocal

def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: SessionLocal) -> schemas.User:
    email = "test@example.com"
    password = "password"
    user_in = schemas.UserCreate(email=email, password=password)
    user = crud.user.create(db=db, obj_in=user_in)
    return user
