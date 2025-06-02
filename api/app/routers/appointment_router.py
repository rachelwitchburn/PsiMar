from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.app import crud, schemas
from api.app.database_app import get_db
from api.app.schemas.appointment import CreateAppointment
from api.app.security import get_current_user
from api.app.models.models import User
from api.app.crud import appointment_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/appointment", tags=["appointment"])

@router.get("/", response_model=list[schemas.appointment.ViewAppointment])
async def get_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna os agendamentos vinculados ao usuário logado,
    seja ele paciente ou profissional.
    """
    if current_user.user_type.value == "professional":
        is_professional = True
    elif current_user.user_type.value == "patient":
        is_professional = False
    else:
        raise HTTPException(status_code=403, detail="Tipo de usuário não autorizado.")

    appointments = crud.appointment_service.appointment_list(
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
    appointment: CreateAppointment,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
        Profissional solicita um novo agendamento com um paciente.

        Requer:
        - Data e horário da consulta.
        - ID do paciente.
        """
    if current_user.user_type.value != "professional":
        raise HTTPException(status_code=403, detail="Apenas profissionais podem acessar esta rota.")

    return crud.appointment_service.request_appointment(
        db=db,
        appointment_date=appointment.date_time,
        patient_id=appointment.patient_id,
        professional_id=current_user.id,
        requested_by="professional"
    )

@router.post("/confirm-professional/{appointment_id}", response_model=schemas.appointment.ViewAppointment)
async def confirm_appointment_professional(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
        Profissional confirma um agendamento solicitado por um paciente.

        Parâmetros:
        - appointment_id: ID do agendamento a ser confirmado.
        """
    if current_user.user_type.value != "professional":
        raise HTTPException(status_code=403, detail="Apenas profissionais podem acessar esta rota.")

    appointment = crud.appointment_service.confirm_appointment_by_professional(
        db=db,
        appointment_id=appointment_id,
        professional_id=current_user.id
    )
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado."
        )
    return appointment

@router.post("/create", response_model=schemas.appointment.ViewAppointment)
async def create_appointment_patient(
    appointment: CreateAppointment,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
       Paciente solicita um novo agendamento com um profissional.

       Requer:
       - Data e horário da consulta.
       - ID do paciente
       """
    if current_user.user_type.value != "patient":
        raise HTTPException(status_code=403, detail="Apenas pacientes podem acessar esta rota.")

    return crud.appointment_service.request_appointment(
        db=db,
        appointment_date=appointment.date_time,
        patient_id=current_user.id,
        professional_id=appointment.professional_id,
        requested_by="patient"
    )

@router.post("/confirm/{appointment_id}", response_model=schemas.appointment.ViewAppointment)
async def confirm_appointment_patient(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
      Paciente confirma um agendamento solicitado por um profissional.

      Parâmetros:
      - appointment_id: ID do agendamento a ser confirmado.
      """
    if current_user.user_type.value != "patient":
        raise HTTPException(status_code=403, detail="Apenas pacientes podem acessar esta rota.")

    appointment = crud.appointment_service.confirm_appointment_by_patient(
        db=db,
        appointment_id=appointment_id,
        patient_id=current_user.id
    )
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado."
        )
    return appointment