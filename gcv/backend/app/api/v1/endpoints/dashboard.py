from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any

from .... import crud, models, schemas
from ....api import deps

router = APIRouter()

@router.get("/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve dashboard statistics.
    """
    counts_data = crud.vulnerability.get_vulnerability_counts_by_severity(db)
    # Formatar para o dicionário esperado
    severity_counts = {severity: count for severity, count in counts_data}

    last_scans = crud.scan.get_last_scans(db)

    return {
        "vulnerability_counts_by_severity": severity_counts,
        "last_five_scans": last_scans,
    }
