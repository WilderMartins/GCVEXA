from pydantic import BaseModel
import datetime
from .user import User
from .scanner_config import ScannerConfig

class ScanBase(BaseModel):
    target_host: str
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

class Scan(ScanInDBBase):
    pass
