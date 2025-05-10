from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlmodel import Session
<<<<<<< Updated upstream
=======
from api.app.models.models import Appointment, AppointmentStatusEnum, Patient, Professional
from api.app.logger_config import logging
logger = logging.getLogger(__name__)
>>>>>>> Stashed changes

from app.models.models import Appointment, Schedule  # conferir erro
from app.schemas.appointment import CreateAppointment, ViewAppointment

<<<<<<< Updated upstream
def create_appointment(db: Session, appointment: CreateAppointment, professional_id: int):
    new_appointment = Appointment(
        date_time=appointment.date_time,
        professional_id=professional_id,
        patient_id=appointment.patient_id,
        status='requested'
    )
    print('agendamento solicitado, aguardando confirmação do paciente')

=======
    # Verifica se o paciente existe
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")

    # Verifica se o profissional existe
    professional = db.query(Professional).filter(Professional.id == professional_id).first()
    if not professional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado.")

    existing = db.query(Appointment).filter(
        Appointment.date_time == appointment_date,
        Appointment.professional_id == professional_id,
        Appointment.status != AppointmentStatusEnum.canceled
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Já existe um agendamento confirmado neste horário.")
>>>>>>> Stashed changes

"""
    def confirm_appointment(db: Session, appointment_id: int, patient: int):
        if Appointment # lógica para confirmar com o paciente, depende dele

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment
    """

# quem faz é o paciente
def request_appointment(db: Session, appointment_date: datetime, patient_id: int):
    new_appointment = Appointment(
        date_time=appointment_date,
        patient_id=patient_id,
        status='requested'
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    print('Agendamento solicitado, aguardando confirmação do profissional')
    return new_appointment

def appointment_list(db: Session, professional_id: int):
    appointments = db.query(Schedule).filter(Schedule.professional_id == professional_id).all()
    return db.query(Schedule).filter(Schedule.professional_id == professional_id).all()
