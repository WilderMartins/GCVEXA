from sqlalchemy import Column, Integer, String, JSON
from ..db.base_class import Base

class ReportTemplate(Base):
    __tablename__ = "report_templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    # config armazena quais seções incluir no relatório
    # e.g., {"include_severity_summary": true, "include_top_hosts": false}
    config = Column(JSON, nullable=False)

class ScheduledReport(Base):
    __tablename__ = "scheduled_reports"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    template_id = Column(Integer, nullable=False)
    # e.g., {"type": "cron", "day_of_week": "mon", "hour": 9}
    schedule_config = Column(JSON, nullable=False)
    # e.g., ["ceo@example.com", "cto@example.com"]
    recipients = Column(JSON, nullable=False)
    is_active = Column(Integer, default=1)
