from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .... import crud, models, schemas
from ....api import deps

router = APIRouter()

@router.get("/", response_model=schemas.Customization)
def read_customization(
    db: Session = Depends(deps.get_db),
):
    """
    Retrieve customization settings (public).
    """
    return crud.customization.get_customization(db)

@router.post("/", response_model=schemas.Customization)
def update_customization(
    *,
    db: Session = Depends(deps.get_db),
    customization_in: schemas.CustomizationUpdate,
    current_user: models.User = Depends(deps.get_current_admin_user),
):
    """
    Update customization settings (Admin only).
    """
    return crud.customization.update_customization(db=db, obj_in=customization_in)
