from pydantic import BaseModel
from sqlalchemy import DATETIME


# quem usa é o psicologo
class CreateAppointment(BaseModel):
    patient_id: int
    date_time: DATETIME

class ViewAppointment(BaseModel):
    id: int
    date_time: DATETIME
    status: str
    professional_id: int
    patient_id: int

    class Config:
        from_attributes = True
        orm_mode = True