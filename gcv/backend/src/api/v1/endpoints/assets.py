from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .... import crud, models, schemas
from ....api import deps

router = APIRouter()

@router.post("/", response_model=schemas.Asset)
def create_asset(
    *,
    db: Session = Depends(deps.get_db),
    asset_in: schemas.AssetCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Create a new asset for the current user.
    """
    return crud.asset.create_asset(db=db, obj_in=asset_in, owner_id=current_user.id)

@router.get("/", response_model=List[schemas.Asset])
def read_assets(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve assets for the current user.
    """
    return crud.asset.get_assets_by_owner(db=db, owner_id=current_user.id)

@router.get("/{asset_id}", response_model=schemas.Asset)
def read_asset(
    *,
    db: Session = Depends(deps.get_db),
    asset_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get an asset by ID.
    """
    asset = crud.asset.get_asset(db, asset_id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if asset.owner_id != current_user.id and not any(role.name == "Admin" for role in current_user.roles):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return asset

@router.put("/{asset_id}", response_model=schemas.Asset)
def update_asset(
    *,
    db: Session = Depends(deps.get_db),
    asset_id: int,
    asset_in: schemas.AssetUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Update an asset owned by the current user.
    """
    asset = crud.asset.get_asset(db, asset_id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if asset.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.asset.update_asset(db=db, db_obj=asset, obj_in=asset_in)

@router.delete("/{asset_id}", response_model=schemas.Asset)
def delete_asset(
    *,
    db: Session = Depends(deps.get_db),
    asset_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Delete an asset owned by the current user.
    """
    asset = crud.asset.get_asset(db, asset_id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if asset.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.asset.delete_asset(db=db, asset_id=asset_id)

@router.get("/{asset_id}/dashboard", response_model=schemas.AssetDashboardStats)
def get_asset_dashboard(
    *,
    db: Session = Depends(deps.get_db),
    asset_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get dashboard statistics for a specific asset.
    """
    asset = crud.asset.get_asset(db, asset_id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    if asset.owner_id != current_user.id and not any(role.name == "Admin" for role in current_user.roles):
        raise HTTPException(status_code=403, detail="Not enough permissions to view this asset's dashboard")

    return crud.asset.get_asset_dashboard_stats(db=db, asset_id=asset_id)
