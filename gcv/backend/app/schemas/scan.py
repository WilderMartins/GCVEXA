from pydantic import BaseModel
import datetime
from .user import User
from .scanner_config import ScannerConfig

class ScanBase(BaseModel):
    asset_id: int
    config_id: int

class ScanCreate(ScanBase):
    pass

class ScanInDBBase(ScanBase):
    id: int
    status: str
    started_at: datetime.datetime
    user: User
    config: ScannerConfig

    class Config:
        orm_mode = True

from .vulnerability import Vulnerability as VulnerabilitySchema
from typing import List

class Scan(ScanInDBBase):
    vulnerabilities: List[VulnerabilitySchema] = []
