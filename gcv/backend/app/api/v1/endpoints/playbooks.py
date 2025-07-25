from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from .... import crud, models, schemas
from ....api import deps
from ....services import playbook_service

router = APIRouter()

@router.post("/", response_model=schemas.Playbook)
def create_playbook(
    *,
    db: Session = Depends(deps.get_db),
    playbook_in: schemas.PlaybookCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
):
    """
    Create a new playbook with its steps and actions. (Admin only)
    """
    return crud.playbook.create_playbook(db=db, obj_in=playbook_in)

@router.get("/", response_model=List[schemas.Playbook])
def read_playbooks(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve all playbooks.
    """
    return crud.playbook.get_all_playbooks(db=db)

@router.post("/run/{vulnerability_id}/{playbook_id}", response_model=schemas.Msg)
async def run_playbook(
    *,
    db: Session = Depends(deps.get_db),
    vulnerability_id: int,
    playbook_id: int,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_analyst_user),
):
    """
    Run a playbook for a specific vulnerability in the background.
    """
    playbook = crud.playbook.get_playbook(db, playbook_id)
    if not playbook:
        raise HTTPException(status_code=404, detail="Playbook not found")

    # Executar em background para não bloquear a resposta da API
    background_tasks.add_task(
        playbook_service.execute_playbook, db, playbook_id, vulnerability_id
    )

    return {"msg": f"Execution of playbook '{playbook.name}' started in the background."}
