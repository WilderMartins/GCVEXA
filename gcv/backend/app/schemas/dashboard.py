from pydantic import BaseModel
from typing import List, Dict
from .scan import Scan

class DashboardStats(BaseModel):
    vulnerability_counts_by_severity: Dict[str, int]
    last_five_scans: List[Scan]

    class Config:
        orm_mode = True
