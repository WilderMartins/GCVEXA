from sqlalchemy.orm import Session
from ..models.customization import Customization
from ..schemas.customization import CustomizationUpdate

def get_customization(db: Session) -> Customization:
    # Sempre busca a configuração com id=1, ou cria se não existir.
    customization = db.query(Customization).filter(Customization.id == 1).first()
    if not customization:
        customization = Customization(id=1, app_title="GCV")
        db.add(customization)
        db.commit()
        db.refresh(customization)
    return customization

def update_customization(db: Session, *, obj_in: CustomizationUpdate) -> Customization:
    db_obj = get_customization(db)
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
