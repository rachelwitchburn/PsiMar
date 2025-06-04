from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime, timezone
from api.app.models.models import AppointmentStatusEnum

#appointmenr.py
# quem usa é o psicologo
class CreateAppointment(BaseModel):
    patient_id: int
    professional_id: int
    date_time: datetime

from datetime import timezone

@field_validator("date_time")
def date_must_be_future(cls, v):
    if v.tzinfo is None:
        v = v.replace(tzinfo=timezone.utc)
    if v <= datetime.now(timezone.utc):
        raise ValueError("A data da consulta deve estar no futuro.")
    return v



class ViewAppointment(BaseModel):
    id: int
    date_time: datetime
    status: AppointmentStatusEnum
    professional_id: int
    patient_id: int

    model_config = ConfigDict(from_attributes=True)
