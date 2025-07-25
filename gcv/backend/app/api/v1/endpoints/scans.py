from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.post("/import", response_model=schemas.Scan)
def import_scan(
    *,
    db: Session = Depends(deps.get_db),
    scan_in: schemas.ScanCreate,
) -> schemas.Scan:
    """
    Import a new scan from a third-party tool.
    """
    scan = crud.scan.create(db=db, obj_in=scan_in)
    return scan
