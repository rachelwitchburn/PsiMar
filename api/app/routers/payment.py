from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.app.crud.payment import create_payment
from api.app.utils.email_service import send_payment_email
from api.app.database_app import get_db
from api.app.models.models import Payment, PaymentStatusEnum
from fastapi import HTTPException

router = APIRouter()

@router.post("/payment/create")
def create_payment_and_notify(appointment_id: int, patient_id: int, professional_id: int, amount: float, method: str, patient_email: str, db: Session = Depends(get_db)):
    payment = create_payment(db, appointment_id, patient_id, professional_id, amount, method)
    send_payment_email(patient_email, amount)
    return {"message": "Pagamento criado e e-mail enviado."}

@router.post("/payment/{payment_id}/confirm")
def confirm_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")

    payment.status = PaymentStatusEnum.completed
    db.commit()
    return {"message": "Pagamento confirmado com sucesso"}