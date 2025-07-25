from pydantic import BaseModel, HttpUrl
from typing import Optional

class ScannerConfigBase(BaseModel):
    name: str
    url: HttpUrl
    username: str
    type: str = "openvas"

class ScannerConfigCreate(ScannerConfigBase):
    password: str

class ScannerConfigUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    username: Optional[str] = None
    password: Optional[str] = None

class ScannerConfigInDBBase(ScannerConfigBase):
    id: int

    class Config:
        orm_mode = True

class ScannerConfig(ScannerConfigInDBBase):
    pass
