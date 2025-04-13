from datetime import datetime, date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.models import Schedule, Appointment


# agenda do psi
def view_schedule_professional(db: Session, professional_id: int):
    return db.query(Appointment) \
        .filter(Appointment.professional_id == professional_id) \
        .filter(Appointment.date_time >= datetime.now()) \
        .order_by(Appointment.date_time).all()

# agenda do paciente
def view_schedule_patient(db: Session, patient_id: int):
    today = date.today()
    result = db.query(Appointment) \
        .filter(Appointment.patient_id == patient_id) \
        .filter(Appointment.date_time >= datetime.combine(today, datetime.min.time())) \
        .filter(Appointment.date_time <= datetime.combine(today, datetime.max.time())) \
        .first()
    return result

