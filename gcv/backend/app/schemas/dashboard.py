from pydantic import BaseModel
from typing import List, Dict, Any
from .scan import Scan

class DashboardStats(BaseModel):
    vulnerability_counts_by_severity: Dict[str, int]
    last_five_scans: List[Scan]

    class Config:
        orm_mode = True

class AdvancedDashboardStats(BaseModel):
    remediation_rate: float
    mean_time_to_remediate: float
    critical_vulns_trend: List[Dict[str, Any]]
    heatmap_data: List[Dict[str, Any]]
