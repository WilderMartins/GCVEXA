from pydantic import BaseModel
from typing import Optional

class AssetBase(BaseModel):
    name: str
    type: str
    address: str

class AssetCreate(AssetBase):
    pass

class AssetUpdate(AssetBase):
    pass

from typing import Dict

class Asset(AssetBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class AssetDashboardStats(BaseModel):
    vulnerability_counts_by_severity: Dict[str, int]
