from sqlalchemy.orm import Session
from .. import models, schemas

def create_playbook(db: Session, *, obj_in: schemas.PlaybookCreate) -> models.Playbook:
    # Cria o playbook principal
    playbook_data = obj_in.dict(exclude={'steps'})
    db_playbook = models.Playbook(**playbook_data)
    db.add(db_playbook)
    db.commit()
    db.refresh(db_playbook)

    # Cria os passos e ações associadas
    for step_in in obj_in.steps:
        step_data = step_in.dict(exclude={'action_config'})
        db_step = models.PlaybookStep(**step_data, playbook_id=db_playbook.id)
        db.add(db_step)
        db.commit()
        db.refresh(db_step)

        action_data = step_in.action_config.dict()
        db_action = models.PlaybookAction(**action_data, step_id=db_step.id)
        db.add(db_action)
        db.commit()

    db.refresh(db_playbook)
    return db_playbook

def get_playbook(db: Session, playbook_id: int) -> models.Playbook:
    return db.query(models.Playbook).filter(models.Playbook.id == playbook_id).first()

def get_all_playbooks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Playbook).offset(skip).limit(limit).all()
