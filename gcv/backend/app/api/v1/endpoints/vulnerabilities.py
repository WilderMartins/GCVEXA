import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .... import crud, models, schemas
from ....api import deps
from ....services import ai_service

router = APIRouter()

@router.post("/{vulnerability_id}/summarize", response_model=schemas.Msg)
def summarize_vulnerability(
    *,
    db: Session = Depends(deps.get_db),
    vulnerability_id: int,
    current_user: models.User = Depends(deps.get_current_analyst_user),
):
    """
    Generate an AI summary for a specific vulnerability.
    """
    vulnerability = db.query(models.Vulnerability).filter(models.Vulnerability.id == vulnerability_id).first()
    if not vulnerability:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    summary = ai_service.summarize_vulnerability(vulnerability)

    return {"msg": summary}

@router.post("/{vulnerability_id}/status", response_model=schemas.Vulnerability)
def update_vulnerability_status(
    *,
    db: Session = Depends(deps.get_db),
    vulnerability_id: int,
    status_in: schemas.VulnerabilityStatusUpdate,
    current_user: models.User = Depends(deps.get_current_analyst_user),
):
    """
    Update the status of a vulnerability.
    """
    vulnerability = db.query(models.Vulnerability).filter(models.Vulnerability.id == vulnerability_id).first()
    if not vulnerability:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    vulnerability.status = status_in.status
    if status_in.status == "remediated":
        vulnerability.remediated_at = datetime.datetime.utcnow()
    else:
        vulnerability.remediated_at = None

    db.add(vulnerability)
    db.commit()
    db.refresh(vulnerability)
    return vulnerability
