from sqlalchemy.orm import Session
from ..models.role import Role

def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()

def get_or_create(db: Session, name: str, description: str = ""):
    role = get_role_by_name(db, name=name)
    if not role:
        role = Role(name=name, description=description)
        db.add(role)
        db.commit()
        db.refresh(role)
    return role
