from sqlalchemy.orm import Session
from .. import models, schemas

def get_asset(db: Session, asset_id: int) -> models.Asset:
    return db.query(models.Asset).filter(models.Asset.id == asset_id).first()

def get_assets_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Asset).filter(models.Asset.owner_id == owner_id).offset(skip).limit(limit).all()

def create_asset(db: Session, *, obj_in: schemas.AssetCreate, owner_id: int) -> models.Asset:
    db_obj = models.Asset(**obj_in.dict(), owner_id=owner_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_asset(db: Session, *, db_obj: models.Asset, obj_in: schemas.AssetUpdate) -> models.Asset:
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_asset(db: Session, *, asset_id: int):
    db_obj = db.query(models.Asset).get(asset_id)
    db.delete(db_obj)
    db.commit()
    return db_obj

def get_asset_dashboard_stats(db: Session, asset_id: int):
    """
    Agrega estatísticas de vulnerabilidade para um único ativo.
    """
    from sqlalchemy import func
    from ..models.vulnerability import VulnerabilityOccurrence, VulnerabilityDefinition

    counts = db.query(VulnerabilityDefinition.severity, func.count(VulnerabilityOccurrence.id)).\
        join(VulnerabilityDefinition).\
        filter(VulnerabilityOccurrence.asset_id == asset_id).\
        group_by(VulnerabilityDefinition.severity).all()

    severity_counts = {severity: count for severity, count in counts}

    # Adicionar outras métricas específicas do ativo aqui...

    return {"vulnerability_counts_by_severity": severity_counts}
