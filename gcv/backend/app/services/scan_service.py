from app import crud, schemas
from app.parsers.dispatcher import get_parser
from sqlalchemy.orm import Session

def import_scan(db: Session, tool: str, scan_data: str) -> schemas.Scan:
    """
    Import a new scan from a third-party tool.
    """
    parser = get_parser(tool)
    scan_in = parser.parse(scan_data)
    scan = crud.scan.create(db=db, obj_in=scan_in)
    return scan
