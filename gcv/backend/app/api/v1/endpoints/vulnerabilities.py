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


from ....models.vulnerability_event import VulnerabilityEvent


@router.post("/{vulnerability_id}/status", response_model=schemas.Vulnerability)
def update_vulnerability_status(
    *,
    db: Session = Depends(deps.get_db),
    vulnerability_id: int,
    status_in: schemas.VulnerabilityStatusUpdate,
    current_user: models.User = Depends(deps.get_current_analyst_user),
):
    """

    Update the status of a vulnerability occurrence.
    """
    occurrence = db.query(models.VulnerabilityOccurrence).filter(models.VulnerabilityOccurrence.id == vulnerability_id).first()
    if not occurrence:
        raise HTTPException(status_code=404, detail="Vulnerability occurrence not found")

    occurrence.status = status_in.status
    if status_in.status == "remediated":
        occurrence.remediated_at = datetime.datetime.utcnow()
    else:
        occurrence.remediated_at = None

    # Criar evento de mudança de status
    event = VulnerabilityEvent(
        occurrence_id=occurrence.id,
        status_change=f"status set to {status_in.status}",
        user_id=current_user.id
    )
    db.add(occurrence)
    db.add(event)
    db.commit()
    db.refresh(occurrence)
    return occurrence

