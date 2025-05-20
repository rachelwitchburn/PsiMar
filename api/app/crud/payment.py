from api.app.models.models import Payment, PaymentStatusEnum
from sqlalchemy.orm import Session

def create_payment(db: Session, appointment_id: int, patient_id: int, professional_id: int, amount: float, method: str):
    payment = Payment(
        appointment_id=appointment_id,
        patient_id=patient_id,
        professional_id=professional_id,
        amount=amount,
        status=PaymentStatusEnum.pending,
        payment_method=method
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
