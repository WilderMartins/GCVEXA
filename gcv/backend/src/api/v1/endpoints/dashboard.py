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
    severity_counts = {severity: count for severity, count in counts_data}
    last_scans = crud.scan.get_last_scans(db)
    return {
        "vulnerability_counts_by_severity": severity_counts,
        "last_five_scans": last_scans,
    }

@router.get("/advanced-stats", response_model=schemas.AdvancedDashboardStats)
def get_advanced_dashboard_stats(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve advanced dashboard statistics.
    """
    remediation_rate = crud.vulnerability.get_remediation_rate(db)
    mttr = crud.vulnerability.get_mttr(db)

    trend_data = crud.vulnerability.get_critical_vulns_trend(db)
    critical_vulns_trend = [{"month": f"{t.year}-{t.month}", "count": t[2]} for t in trend_data]

    heatmap_raw_data = crud.vulnerability.get_heatmap_data(db)
    heatmap_data = [{"host": h, "severity": s, "count": c} for h, s, c in heatmap_raw_data]

    return {
        "remediation_rate": remediation_rate,
        "mean_time_to_remediate": mttr,
        "critical_vulns_trend": critical_vulns_trend,
        "heatmap_data": heatmap_data,
    }
