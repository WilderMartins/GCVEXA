from sqlalchemy.orm import Session

from ..core.security import get_password_hash
from ..models.user import User
from ..schemas.user import UserCreate


def get_user_by_email(db: Session, *, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, *, obj_in: UserCreate):
    db_obj = User(
        email=obj_in.email,
        full_name=obj_in.full_name,
        hashed_password=get_password_hash(obj_in.password),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
