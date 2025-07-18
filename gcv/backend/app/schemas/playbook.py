from pydantic import BaseModel, Json
from typing import List, Optional

# --- Schemas para Ações ---
class PlaybookActionBase(BaseModel):
    config: Json

class PlaybookActionCreate(PlaybookActionBase):
    pass

class PlaybookAction(PlaybookActionBase):
    id: int
    class Config:
        orm_mode = True

# --- Schemas para Passos ---
class PlaybookStepBase(BaseModel):
    step_number: int
    action_type: str

class PlaybookStepCreate(PlaybookStepBase):
    action_config: PlaybookActionCreate

class PlaybookStep(PlaybookStepBase):
    id: int
    action_config: Optional[PlaybookAction] = None
    class Config:
        orm_mode = True

# --- Schemas para Playbooks ---
class PlaybookBase(BaseModel):
    name: str
    description: Optional[str] = None

class PlaybookCreate(PlaybookBase):
    steps: List[PlaybookStepCreate] = []

class PlaybookUpdate(PlaybookBase):
    pass

class Playbook(PlaybookBase):
    id: int
    steps: List[PlaybookStep] = []
    class Config:
        orm_mode = True

# --- Schemas para Execução ---
class PlaybookExecution(BaseModel):
    id: int
    status: str
    playbook_id: int
    vulnerability_id: int
    class Config:
        orm_mode = True
