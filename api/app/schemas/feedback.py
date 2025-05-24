# gestao de feedback

from pydantic import BaseModel, model_validator, ConfigDict
from datetime import datetime
from typing import Optional

class FeedbackCreate(BaseModel):
    message: str
    patient_id: int
    professional_id: int


class FeedbackRead(BaseModel):
    id: int
    message: str
    date: datetime
    patient_id: int
    professional_id: int

    model_config = ConfigDict(from_attributes=True)