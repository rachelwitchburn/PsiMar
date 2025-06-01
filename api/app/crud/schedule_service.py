from datetime import datetime, date, time, timezone
import logging
from sqlalchemy.orm import Session
from api.app.models.models import Appointment

logger = logging.getLogger(__name__)

# agenda do psi
def get_schedule_professional(db: Session, professional_id: int):
    logger.info(f"Buscando agenda para profissional com ID {professional_id}")
    return db.query(Appointment) \
        .filter(Appointment.professional_id == professional_id) \
        .filter(Appointment.date_time >= datetime.now(timezone.utc)) \
        .order_by(Appointment.date_time).all()

# agenda do paciente
def get_schedule_patient(db: Session, patient_id: int):
    logger.info(f"Buscando agenda do dia para paciente com ID {patient_id}")
    today = date.today()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    return db.query(Appointment) \
        .filter(Appointment.patient_id == patient_id) \
        .filter(Appointment.date_time >= start_of_day) \
        .filter(Appointment.date_time <= end_of_day) \
        .order_by(Appointment.date_time) \
        .all()


