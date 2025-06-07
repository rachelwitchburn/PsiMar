from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.app import schemas
from api.app.database_app import get_db
from api.app.security import get_current_user
from api.app.models.models import User
from api.app.crud import appointment_service
import logging


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/appointment", tags=["appointment"])

def get_is_professional(user: User) -> bool:
    if user.user_type.value == "professional":
        return True
    elif user.user_type.value == "patient":
        return False
    else:
        raise HTTPException(status_code=403, detail="Tipo de usuário não autorizado.")

def ensure_professional(user: User):
    if user.user_type.value != "professional":
        raise HTTPException(status_code=403, detail="Apenas profissionais podem acessar esta rota.")

def ensure_patient(user: User):
    if user.user_type.value != "patient":
        raise HTTPException(status_code=403, detail="Apenas pacientes podem acessar esta rota.")

@router.get("/", response_model=list[schemas.appointment.ViewAppointment])
async def get_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
       Retorna os agendamentos vinculados ao usuário logado.
    """
    is_professional = get_is_professional(current_user)

    appointments = appointment_service.appointment_list(
        db=db,
        user_id=current_user.id,
        is_professional=is_professional
    )

    if not appointments:
        logger.info(f"Usuário '{current_user.email}' não possui agendamentos.")
    else:
        logger.info(f"Usuário '{current_user.email}' possui {len(appointments)} agendamento(s).")

    return appointments


@router.post("/create-professional", response_model=schemas.appointment.ViewAppointment)
async def create_appointment_professional(
    appointment: schemas.appointment.CreateAppointment,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
        Profissional solicita um novo agendamento com um paciente.
    """
    ensure_professional(current_user)

    return appointment_service.request_appointment(
        db=db,
        appointment_date=appointment.date_time,
        patient_id=appointment.patient_id,
        professional_id=current_user.id,
        requested_by_id=current_user.id
    )



@router.post("/create", response_model=schemas.appointment.ViewAppointment)
async def create_appointment_patient(
    appointment: schemas.appointment.CreateAppointment,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
       Paciente solicita um novo agendamento com um profissional.
    """

    ensure_patient(current_user)

    return appointment_service.request_appointment(
        db=db,
        appointment_date=appointment.date_time,
        patient_id=current_user.id,
        professional_id=appointment.professional_id,
        requested_by_id=current_user.id
    )

@router.post("/confirm-professional/{appointment_id}", response_model=schemas.appointment.ViewAppointment)
async def confirm_appointment_professional(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Profissional confirma um agendamento solicitado por um paciente.
    """
    ensure_professional(current_user)

    return appointment_service.confirm_appointment(
        db=db,
        appointment_id=appointment_id,
        user=current_user
    )

@router.post("/confirm/{appointment_id}", response_model=schemas.appointment.ViewAppointment)
async def confirm_appointment_patient(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Paciente confirma um agendamento solicitado por um profissional.
    """
    ensure_patient(current_user)

    return appointment_service.confirm_appointment(
        db=db,
        appointment_id=appointment_id,
        user=current_user
    )