from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any

from .... import crud, models, schemas
from ....api import deps
from ....services.gvm_service import GVMService
from ....schemas.msg import Msg

router = APIRouter()

@router.post("/test-connection", response_model=Msg)
def test_scanner_connection(
    *,
    config_in: schemas.ScannerConfigCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Test connection to a scanner with provided credentials. (Admin only)
    """
    # Criamos um objeto de modelo falso para passar para o serviço
    fake_config_model = models.ScannerConfig(
        url=str(config_in.url),
        username=config_in.username,
        encrypted_password=crud.scanner_config.encrypt_data(config_in.password)
    )
    service = GVMService(fake_config_model)
    is_success, message = service.test_connection()
    if not is_success:
        raise HTTPException(
            status_code=400,
            detail=f"Connection failed: {message}",
        )
    return {"msg": f"Connection successful! GVM version: {message}"}


@router.post("/", response_model=schemas.ScannerConfig)
def create_scanner_config(
    *,
    db: Session = Depends(deps.get_db),
    config_in: schemas.ScannerConfigCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
):
    """
    Create new scanner configuration. (Admin only)
    """
    config = crud.scanner_config.get_config_by_name(db, name=config_in.name)
    if config:
        raise HTTPException(
            status_code=400,
            detail="A scanner configuration with this name already exists.",
        )
    config = crud.scanner_config.create_config(db=db, obj_in=config_in)
    return config

@router.get("/", response_model=List[schemas.ScannerConfig])
def read_scanner_configs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve scanner configurations.
    """
    configs = crud.scanner_config.get_all_configs(db, skip=skip, limit=limit)
    return configs

@router.put("/{config_id}", response_model=schemas.ScannerConfig)
def update_scanner_config(
    *,
    db: Session = Depends(deps.get_db),
    config_id: int,
    config_in: schemas.ScannerConfigUpdate,
    current_user: models.User = Depends(deps.get_current_admin_user),
):
    """
    Update a scanner configuration. (Admin only)
    """
    config = crud.scanner_config.get_config(db, config_id=config_id)
    if not config:
        raise HTTPException(
            status_code=404,
            detail="Scanner configuration not found.",
        )
    config = crud.scanner_config.update_config(db=db, db_obj=config, obj_in=config_in)
    return config
