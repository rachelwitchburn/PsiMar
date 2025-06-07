from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from api.app.schemas.payment import PaymentCreate, PaymentOut
from api.app.crud import payment_service
from api.app.database_app import get_db
from api.app.utils.email_utils import send_email
from api.app.models.models import PaymentStatusEnum
import logging


logger = logging.getLogger(__name__)


# payment_router.py
router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentOut)
async def make_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Tentando criar pagamento: {payment}")
        db_payment = payment_service.create_payment(db, payment)
        logger.info(f"Pagamento criado com sucesso: ID {db_payment.id}")
        return db_payment
    except HTTPException as e:
        raise e
    except IntegrityError:
        db.rollback()
        logger.exception("Erro de integridade ao processar o pagamento")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro de integridade ao processar o pagamento.")
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro no banco de dados ao processar o pagamento")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro no banco de dados.")
    except Exception as e:
        db.rollback()
        logger.exception("Erro inesperado ao processar o pagamento")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro inesperado ao processar o pagamento.")


@router.post("/{payment_id}/confirm", response_model=PaymentOut)
async def confirm_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        payment = payment_service.update_payment_status(db, payment_id, status=PaymentStatusEnum.completed)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado")

        if not payment.patient or not payment.patient.user or not payment.patient.user.email:
            logger.warning(f"Pagamento {payment_id} confirmado, mas paciente ou email ausente.")
            return payment

        patient_email = payment.patient.user.email
        subject = "Confirmação de Pagamento"
        content = f"Olá {payment.patient.user.first_name}, seu pagamento de R$ {payment.amount:.2f} foi confirmado com sucesso!"

        try:
            await send_email(patient_email, subject, content)
        except Exception as email_err:
            logger.exception(f"Falha ao enviar email de confirmação para {patient_email}: {email_err}")
            return payment

        return payment

    except HTTPException as e:
        raise e

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Erro no banco de dados ao confirmar pagamento")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Erro ao acessar o banco de dados.")

    except Exception as e:
        db.rollback()
        logger.exception("Erro inesperado ao confirmar pagamento")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Erro inesperado ao confirmar pagamento.")


@router.get("/{payment_id}", response_model=PaymentOut)
async def get_payment(payment_id: int, db: Session = Depends(get_db)):
    try:
        payment = payment_service.get_payment(db, payment_id)
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pagamento não encontrado")
        return payment

    except HTTPException as e:
        raise e

    except SQLAlchemyError:
        logger.exception("Erro no banco de dados ao obter pagamento")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Erro ao acessar o banco de dados.")

    except Exception as e:
        logger.exception("Erro inesperado ao obter pagamento")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Erro inesperado ao obter pagamento.")

