# gestao de feedback

from pydantic import BaseModel, model_validator, ConfigDict
from datetime import datetime


class FeedbackCreate(BaseModel):
    message: str
    rating: int
    patient_id: int
    professional_id: int

    @model_validator(mode="after")
    def validate_rating(cls, model):
        if not (0 <= model.rating <= 5):
            raise ValueError('Rating deve ser entre 0 e 5.')
        return model

class FeedbackRead(BaseModel):
    id: int
    message: str
    rating: int
    date: datetime
    patient_id: int
    professional_id: int

    model_config = ConfigDict(from_attributes=True)