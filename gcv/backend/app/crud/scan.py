from sqlalchemy.orm import Session
from ..models.scan import Scan
from ..schemas.scan import ScanCreate
from ..models.user import User

def create_scan(db: Session, *, obj_in: ScanCreate, user: User):
    db_obj = Scan(
        target_host=obj_in.target_host,
        config_id=obj_in.config_id,
        user_id=user.id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_scan(db: Session, scan_id: int):
    return db.query(Scan).filter(Scan.id == scan_id).first()

def get_all_scans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Scan).offset(skip).limit(limit).all()

def update_scan_status(db: Session, scan_id: int, status: str, gvm_task_id: str = None):
    db_obj = get_scan(db, scan_id=scan_id)
    if db_obj:
        db_obj.status = status
        if gvm_task_id:
            db_obj.gvm_task_id = gvm_task_id
        db.commit()
        db.refresh(db_obj)
    return db_obj
