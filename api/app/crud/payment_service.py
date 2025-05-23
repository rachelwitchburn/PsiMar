from sqlalchemy.orm import Session
from api.app.models.models import Payment
from api.app.schemas.payment import PaymentCreate

def create_payment(db: Session, payment: PaymentCreate):
    db_payment = Payment(
        patient_id=payment.patient_id,
        professional_id=payment.professional_id,
        amount=payment.amount
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()

def update_payment_status(db: Session, payment_id: int, status: str):
    payment = get_payment(db, payment_id)
    if payment:
        payment.status = status
        db.commit()
        db.refresh(payment)
    return payment