from pydantic import BaseModel, ConfigDict


from api.app.models.models import PaymentMethodEnum, PaymentStatusEnum


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
    appointment_id: int
    amount: float
    payment_method: PaymentMethodEnum
    status: PaymentStatusEnum

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)