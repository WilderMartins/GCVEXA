from pydantic import BaseModel
from typing import Optional

class CustomizationBase(BaseModel):
    app_title: Optional[str] = None
    logo_base64: Optional[str] = None

class CustomizationCreate(CustomizationBase):
    pass

class CustomizationUpdate(CustomizationBase):
    pass

class CustomizationInDBBase(CustomizationBase):
    id: int

    class Config:
        orm_mode = True

class Customization(CustomizationInDBBase):
    pass
