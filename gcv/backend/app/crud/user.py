from sqlalchemy.orm import Session
from . import role
from ..core.security import get_password_hash
from ..models.user import User
from ..schemas.user import UserCreate

def get_user_by_email(db: Session, *, email: str):
    return db.query(User).filter(User.email == email).first()

def get_all_users_count(db: Session) -> int:
    return db.query(User.id).count()

def create_user(db: Session, *, obj_in: UserCreate):
    db_obj = User(
        email=obj_in.email,
        full_name=obj_in.full_name,
        hashed_password=get_password_hash(obj_in.password),
    )

    # Assign role
    user_count = get_all_users_count(db)
    if user_count == 0:
        admin_role = role.get_role_by_name(db, name="Admin")
        if admin_role:
            db_obj.roles.append(admin_role)
    else:
        analyst_role = role.get_role_by_name(db, name="Analyst")
        if analyst_role:
            db_obj.roles.append(analyst_role)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
