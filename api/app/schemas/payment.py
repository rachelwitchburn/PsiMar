from pydantic import BaseModel, ConfigDict

#payment.py
from api.app.models.models import PaymentMethodEnum


class PaymentCreate(BaseModel):
    patient_id: int
    professional_id: int
    amount: float
    payment_method: PaymentMethodEnum

class PaymentOut(BaseModel):
    id: int
    patient_id: int
    professional_id: int
    amount: float
    status: str

    model_config = ConfigDict(from_attributes=True)