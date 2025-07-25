from sqlalchemy.orm import Session
from ..core.encryption import encrypt_data, decrypt_data
from ..models.scanner_config import ScannerConfig
from ..schemas.scanner_config import ScannerConfigCreate, ScannerConfigUpdate

def get_config(db: Session, config_id: int):
    return db.query(ScannerConfig).filter(ScannerConfig.id == config_id).first()

def get_config_by_name(db: Session, name: str):
    return db.query(ScannerConfig).filter(ScannerConfig.name == name).first()

def get_all_configs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ScannerConfig).offset(skip).limit(limit).all()

def create_config(db: Session, *, obj_in: ScannerConfigCreate):
    encrypted_password = encrypt_data(obj_in.password)
    db_obj = ScannerConfig(
        name=obj_in.name,
        url=str(obj_in.url),
        username=obj_in.username,
        encrypted_password=encrypted_password,
        type=obj_in.type
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_config(db: Session, *, db_obj: ScannerConfig, obj_in: ScannerConfigUpdate):
    update_data = obj_in.dict(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        encrypted_password = encrypt_data(update_data["password"])
        del update_data["password"]
        update_data["encrypted_password"] = encrypted_password

    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
