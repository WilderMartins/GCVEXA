from sqlalchemy.orm import Session
from .. import models
from . import pdf_service, email_service
from ..db.session import SessionLocal

async def generate_and_send_report(scheduled_report_id: int):
    """
    A tarefa que é executada pelo APScheduler.
    """
    print(f"Running scheduled report job for ID: {scheduled_report_id}")
    db: Session = SessionLocal()
    try:
        scheduled_report = db.query(models.reporting.ScheduledReport).filter(models.reporting.ScheduledReport.id == scheduled_report_id).first()
        if not scheduled_report or not scheduled_report.is_active:
            print(f"Scheduled report {scheduled_report_id} not found or is inactive. Skipping.")
            return

        template = db.query(models.reporting.ReportTemplate).filter(models.reporting.ReportTemplate.id == scheduled_report.template_id).first()
        if not template:
            print(f"Template {scheduled_report.template_id} not found. Skipping.")
            return

        # Gerar o PDF
        pdf_buffer = pdf_service.create_advanced_report(db, template)
        pdf_filename = f"{template.name.replace(' ', '_')}.pdf"

        # Enviar por e-mail
        # (O email_service precisaria ser adaptado para enviar anexos)
        print(f"Report '{pdf_filename}' generated. Would be sent to: {scheduled_report.recipients}")
        # await email_service.send_report_email(
        #     recipients=scheduled_report.recipients,
        #     subject=f"Your Scheduled GCV Report: {template.name}",
        *#     pdf_attachment=pdf_buffer,
        #     pdf_filename=pdf_filename
        # )

    finally:
        db.close()
