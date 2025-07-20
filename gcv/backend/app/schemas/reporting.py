from pydantic import BaseModel, Json
from typing import List, Optional

class ReportTemplateBase(BaseModel):
    name: str
    config: Json

class ReportTemplateCreate(ReportTemplateBase):
    pass

class ReportTemplate(ReportTemplateBase):
    id: int
    class Config:
        orm_mode = True

class ScheduledReportBase(BaseModel):
    name: str
    template_id: int
    schedule_config: Json # e.g., {"type": "cron", "day_of_week": "mon", "hour": 9}
    recipients: List[str]
    is_active: bool = True

class ScheduledReportCreate(ScheduledReportBase):
    pass

class ScheduledReport(ScheduledReportBase):
    id: int
    class Config:
        orm_mode = True
