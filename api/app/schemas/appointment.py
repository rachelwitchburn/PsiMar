from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime

# quem usa é o psicologo
class CreateAppointment(BaseModel):
    patient_id: int
    professional_id: int
    date_time: datetime

    @field_validator("date_time")
    def date_must_be_future(cls, v):
        if v <= datetime.now():
            raise ValueError("A data da consulta deve estar no futuro.")
        return v

class ViewAppointment(BaseModel):
    id: int
    date_time: datetime
    status: str
    professional_id: int
    patient_id: int

    model_config = ConfigDict(from_attributes=True)
