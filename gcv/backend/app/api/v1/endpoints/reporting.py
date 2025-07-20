from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .... import crud, models, schemas
from ....api import deps

router = APIRouter()

# Endpoints para Templates
@router.post("/templates/", response_model=schemas.ReportTemplate)
def create_report_template(
    *,
    db: Session = Depends(deps.get_db),
    template_in: schemas.ReportTemplateCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
):
    return crud.reporting.create_template(db=db, obj_in=template_in)

@router.get("/templates/", response_model=List[schemas.ReportTemplate])
def read_report_templates(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return crud.reporting.get_all_templates(db=db)

# Endpoints para Scheduled Reports
@router.post("/schedules/", response_model=schemas.ScheduledReport)
def create_scheduled_report(
    *,
    db: Session = Depends(deps.get_db),
    schedule_in: schemas.ScheduledReportCreate,
    current_user: models.User = Depends(deps.get_current_admin_user),
):
    return crud.reporting.create_scheduled_report(db=db, obj_in=schedule_in)

@router.get("/schedules/", response_model=List[schemas.ScheduledReport])
def read_scheduled_reports(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_admin_user),
):
    return crud.reporting.get_all_scheduled_reports(db=db)

@router.delete("/schedules/{report_id}")
def delete_scheduled_report(
    *,
    db: Session = Depends(deps.get_db),
    report_id: int,
    current_user: models.User = Depends(deps.get_current_admin_user),
):
    crud.reporting.delete_scheduled_report(db=db, report_id=report_id)
    return {"msg": "Scheduled report deleted successfully."}
