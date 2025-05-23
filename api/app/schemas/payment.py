from pydantic import BaseModel, ConfigDict


class PaymentCreate(BaseModel):
    patient_id: int
    professional_id: int
    amount: float

class PaymentOut(BaseModel):
    id: int
    patient_id: int
    professional_id: int
    amount: float
    status: str

    model_config = ConfigDict(from_attributes=True)