from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session
from api.app.models.models import Appointment, AppointmentStatusEnum, Patient, Professional, User
from api.app.logger_config import logging
logger = logging.getLogger(__name__)

#appointment_service.py
def request_appointment(db: Session, appointment_date: datetime, patient_id: int, professional_id: int, requested_by_id: int):

    # Verifica se o paciente existe
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")

    # Verifica se o profissional existe
    professional = db.query(Professional).filter(Professional.id == professional_id).first()
    if not professional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado.")

    # Verifica conflito de horário
    existing = db.query(Appointment).filter(
        Appointment.date_time == appointment_date,
        Appointment.professional_id == professional_id,
        Appointment.status != AppointmentStatusEnum.canceled
    ).first()

    if existing:
        logger.warning(f"Conflito de agendamento: Profissional {professional_id} já possui agendamento confirmado neste horário {appointment_date}.")
        raise HTTPException(status_code=409, detail="Já existe um agendamento confirmado neste horário.")

    new_appointment = Appointment(
        date_time=appointment_date,
        patient_id=patient_id,
        professional_id=professional_id,
        status=AppointmentStatusEnum.requested,
        requested_by_id = requested_by_id
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    logger.info(f'Agendamento solicitado pelo usuário {requested_by_id}, aguardando confirmação.')

    return new_appointment

def confirm_appointment(db: Session, appointment_id: int, user: User):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")

    if appointment.status != AppointmentStatusEnum.requested:
        raise HTTPException(status_code=400, detail="Agendamento não está mais pendente.")

    if appointment.requested_by_id == user.id:
        raise HTTPException(status_code=403, detail="Você não pode confirmar um agendamento que solicitou. Aguarde a confirmação da outra parte.")

    if user.user_type.value == "patient" and appointment.patient_id != user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para confirmar este agendamento.")

    if user.user_type.value == "professional" and appointment.professional_id != user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para confirmar este agendamento.")

    previous_status = appointment.status
    appointment.status = AppointmentStatusEnum.confirmed
    db.commit()
    db.refresh(appointment)

    logger.info(f'Agendamento {appointment_id} alterado de {previous_status} para {appointment.status} pelo {user.user_type.value} (usuário {user.id}).')

    return appointment



def appointment_list(db: Session, user_id: int, is_professional: bool):
    if is_professional:
        appointments = db.query(Appointment).filter(
            Appointment.professional_id == user_id
        ).order_by(Appointment.date_time.desc()).all()
    else:
        appointments = db.query(Appointment).filter(
            Appointment.patient_id == user_id
        ).order_by(Appointment.date_time.desc()).all()

    return appointments
