from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .... import crud, schemas
from ....api import deps

router = APIRouter()

@router.get("/status")
def get_setup_status(db: Session = Depends(deps.get_db)):
    """
    Check if the initial setup needs to be performed.
    Returns true if no users exist in the database.
    """
    user_count = crud.user.get_all_users_count(db)
    return {"needs_setup": user_count == 0}

@router.post("/initialize")
def initialize_setup(
    *,
    db: Session = Depends(deps.get_db),
    setup_in: schemas.UserCreate, # Reutilizar o schema de criação de usuário
):
    """
    Perform the initial setup by creating the first Admin user.
    This endpoint will fail if users already exist.
    """
    user_count = crud.user.get_all_users_count(db)
    if user_count > 0:
        raise HTTPException(
            status_code=400,
            detail="Setup has already been completed.",
        )

    # A lógica em crud.user.create_user já atribui o papel de Admin ao primeiro usuário
    user = crud.user.create_user(db=db, obj_in=setup_in)

    return {"msg": f"Admin user {user.email} created successfully. Please log in."}
