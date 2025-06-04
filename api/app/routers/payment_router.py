from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.app.schemas.payment import PaymentCreate, PaymentOut
from api.app.crud import payment_service
from api.app.database_app import get_db
from api.app.utils.email_utils import send_email

# payment_router.py
router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentOut)
async def make_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = payment_service.create_payment(db, payment)
    return db_payment


@router.post("/{payment_id}/confirm", response_model=PaymentOut)
async def confirm_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = payment_service.update_payment_status(db, payment_id, status="completed")
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")

    # Buscar e-mail do paciente
    patient_email = payment.patient.user.email
    subject = "Confirmação de Pagamento"
    content = f"Olá {payment.patient.user.first_name}, seu pagamento de R$ {payment.amount:.2f} foi confirmado com sucesso!"

    # Envia e-mail
    await send_email(patient_email, subject, content)

    return payment

@router.get("/{payment_id}", response_model=PaymentOut)
async def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = payment_service.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return payment

