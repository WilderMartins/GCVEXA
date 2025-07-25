from sqlalchemy.orm import Session
from .. import models, schemas
from ..core.scheduler import scheduler
from ..services.reporting_tasks import generate_and_send_report

# Template CRUD
def create_template(db: Session, *, obj_in: schemas.ReportTemplateCreate) -> models.reporting.ReportTemplate:
    db_obj = models.reporting.ReportTemplate(**obj_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_all_templates(db: Session):
    return db.query(models.reporting.ReportTemplate).all()

# Scheduled Report CRUD
def create_scheduled_report(db: Session, *, obj_in: schemas.ScheduledReportCreate) -> models.reporting.ScheduledReport:
    db_obj = models.reporting.ScheduledReport(**obj_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    # Adicionar o job ao scheduler
    if db_obj.is_active:
        schedule_conf = db_obj.schedule_config
        scheduler.add_job(
            generate_and_send_report,
            id=f"report_{db_obj.id}",
            kwargs={"scheduled_report_id": db_obj.id},
            trigger=schedule_conf.pop("type", "cron"),
            **schedule_conf,
            replace_existing=True
        )
    return db_obj

def update_scheduled_report(db: Session, *, db_obj: models.reporting.ScheduledReport, obj_in: schemas.ScheduledReportCreate) -> models.reporting.ScheduledReport:
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    # Atualizar o job no scheduler
    job = scheduler.get_job(f"report_{db_obj.id}")
    if db_obj.is_active:
        schedule_conf = db_obj.schedule_config
        if job:
            job.reschedule(trigger=schedule_conf.pop("type", "cron"), **schedule_conf)
        else:
            scheduler.add_job(
                generate_and_send_report,
                id=f"report_{db_obj.id}",
                kwargs={"scheduled_report_id": db_obj.id},
                trigger=schedule_conf.pop("type", "cron"),
                **schedule_conf
            )
    elif job:
        scheduler.remove_job(f"report_{db_obj.id}")

    return db_obj

def delete_scheduled_report(db: Session, *, report_id: int):
    db_obj = db.query(models.reporting.ScheduledReport).get(report_id)
    if db_obj:
        # Remover do scheduler
        if scheduler.get_job(f"report_{report_id}"):
            scheduler.remove_job(f"report_{report_id}")
        db.delete(db_obj)
        db.commit()
    return db_obj

def get_all_scheduled_reports(db: Session):
    return db.query(models.reporting.ScheduledReport).all()
