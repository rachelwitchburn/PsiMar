from pydantic import BaseModel, ConfigDict
from enum import Enum as PyEnum

class PaymentMethodEnum(str, PyEnum):
    card = "card"
    transfer = "transfer"
    cash = "cash"
    pix = "pix"

class PaymentCreate(BaseModel):
    patient_id: int
    professional_id: int
    appointment_id: int
    amount: float
    payment_method: PaymentMethodEnum

class PaymentOut(BaseModel):
    id: int
    patient_id: int
    professional_id: int
    amount: float
    status: str
    payment_method: PaymentMethodEnum

    model_config = ConfigDict(from_attributes=True)