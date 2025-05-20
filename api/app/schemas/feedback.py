# gestao de feedback

from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class FeedbackCreate(BaseModel):
    message: str
    patient_id: Optional[int] = None
    priority: Optional[int] = None

class FeedbackRead(BaseModel):
    id: int
    message: str
    date: datetime
    patient_id: Optional[int] = None
    professional_id: Optional[int] = None

    class Config:
        orm_mode = True