from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session
from api.app.models.models import Appointment
from api.app.logger_config import logging
logger = logging.getLogger(__name__)

def request_appointment(db: Session, appointment_date: datetime, patient_id: int, professional_id: int, requested_by: str):
    if requested_by not in ['patient', 'professional']:
        raise ValueError("O campo 'requested_by' deve ser 'patient' ou 'professional'.")

    existing = db.query(Appointment).filter(
    Appointment.date_time == appointment_date,
    Appointment.status == 'confirmed',
    ((Appointment.patient_id == patient_id) | (Appointment.professional_id == professional_id))
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Já existe um agendamento confirmado neste horário.")

    new_appointment = Appointment(
        date_time=appointment_date,
        patient_id=patient_id,
        professional_id=professional_id,
        status='requested'
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    if requested_by == 'patient':
        logger.info('Agendamento solicitado pelo paciente, aguardando confirmação do profissional.')
    else:
        logger.info('Agendamento solicitado pelo profissional, aguardando confirmação do paciente.')

    return new_appointment

def confirm_appointment(db: Session, appointment_id: int, user_id: int, user_type: str):
    if user_type not in ['patient', 'professional']:
        raise ValueError("user_type deve ser 'patient' ou 'professional'")

    filter_field = Appointment.patient_id if user_type == 'patient' else Appointment.professional_id
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id, filter_field == user_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado ou acesso negado.")

    if appointment.status != 'requested':
        raise HTTPException(status_code=400, detail="Agendamento não está mais pendente.")

    appointment.status = 'confirmed'
    db.commit()
    db.refresh(appointment)
    return appointment


def confirm_appointment_by_professional(db, appointment_id, professional_id):
    return confirm_appointment(db, appointment_id, professional_id, 'professional')

def confirm_appointment_by_patient(db, appointment_id, patient_id):
    return confirm_appointment(db, appointment_id, patient_id, 'patient')


def appointment_list(db: Session, user_id: int, is_professional: bool):
    if is_professional:
        appointments = db.query(Appointment).filter(Appointment.professional_id == user_id).order_by(Appointment.date_time.desc()).all()
    else:
        appointments = db.query(Appointment).filter(Appointment.patient_id == user_id).order_by(Appointment.date_time.desc()).all()

    return appointments
