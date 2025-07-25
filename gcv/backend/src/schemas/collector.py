from pydantic import BaseModel
from typing import Dict, Any

class CollectorBase(BaseModel):
    name: str
    tool: str
    collector_type: str
    config: Dict[str, Any]

class CollectorCreate(CollectorBase):
    pass

class Collector(CollectorBase):
    id: int

    class Config:
        orm_mode = True
