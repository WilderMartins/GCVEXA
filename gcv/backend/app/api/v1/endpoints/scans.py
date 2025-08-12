from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app import schemas
from app.api import deps
from app.services import scan_service

router = APIRouter()

@router.post("/import", response_model=schemas.Scan)
def import_scan(
    *,
    db: Session = Depends(deps.get_db),
    tool: str,
    file: UploadFile = File(...),
) -> schemas.Scan:
    """
    Import a new scan from a third-party tool.
    """
    try:
        scan_data = file.file.read().decode("utf-8")
        scan = scan_service.import_scan(db, tool, scan_data)
        return scan
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
