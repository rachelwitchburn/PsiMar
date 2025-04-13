from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlmodel import Session

from app.models.models import Appointment, Schedule  # conferir erro
from app.schemas.appointment import CreateAppointment, ViewAppointment

def create_appointment(db: Session, appointment: CreateAppointment, professional_id: int):
    new_appointment = Appointment(
        date_time=appointment.date_time,
        professional_id=professional_id,
        patient_id=appointment.patient_id,
        status='requested'
    )
    print('agendamento solicitado, aguardando confirmação do paciente')


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
