from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from app.parsers.dispatcher import get_parser

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
        parser = get_parser(tool)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    scan_data = file.file.read().decode("utf-8")
    scan_in = parser.parse(scan_data)
    scan = crud.scan.create(db=db, obj_in=scan_in)
    return scan
