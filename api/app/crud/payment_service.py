from sqlalchemy.orm import Session
from api.app.models.models import Payment
from api.app.schemas.payment import PaymentCreate
from api.app.models.models import PaymentStatusEnum
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError


def create_payment(db: Session, payment: PaymentCreate):
    existing_payment = db.query(Payment).filter(
        Payment.appointment_id == payment.appointment_id,
        Payment.status.in_([PaymentStatusEnum.pending, PaymentStatusEnum.completed])
    ).first()

    if existing_payment:
        raise HTTPException(status_code=409, detail="Já existe um pagamento para esta consulta.")

    db_payment = Payment(
        patient_id=payment.patient_id,
        professional_id=payment.professional_id,
        appointment_id=payment.appointment_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status=PaymentStatusEnum.pending

    )
    try:
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar pagamento.")

    return db_payment

def get_payment(db: Session, payment_id: int):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado.")
    return payment

def update_payment_status(db: Session, payment_id: int, status: PaymentStatusEnum):
    payment = get_payment(db, payment_id)
    try:
        payment.status = status
        db.commit()
        db.refresh(payment)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar status do pagamento.")
    return payment