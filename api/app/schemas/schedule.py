from datetime import datetime
from pydantic import BaseModel



# quem usa é o psicologo
class Schedule(BaseModel):
    id: int
    date_time: datetime
    status: str
    professional_id: int
    patient_id: int

    class Config:
        from_attributes = True
        orm_mode = True
