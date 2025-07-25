from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True

class Role(BaseModel):
    name: str
    class Config:
        orm_mode = True

class User(UserInDBBase):
    mfa_enabled: bool
    roles: list[Role] = []

class UserInDB(UserInDBBase):
    hashed_password: str
