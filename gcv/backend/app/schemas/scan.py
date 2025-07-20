import datetime
from pydantic import BaseModel
from typing import List

from .user import User
from .scanner_config import ScannerConfig
from .asset import Asset
from .vulnerability import VulnerabilityOccurrenceBase

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
    asset: Asset

    class Config:
        orm_mode = True

class Scan(ScanInDBBase):
    vulnerabilities: List[VulnerabilityOccurrenceBase] = []