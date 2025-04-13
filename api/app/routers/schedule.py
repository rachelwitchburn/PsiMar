from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database_app import get_db
from app.models.models import User, UserTypeEnum, Appointment
from app.security import get_current_user

router = APIRouter(prefix="/schedule", tags=["Schedule"])

@router.get("/professional/schedule")
def get_professional_schedule(db: Session = Depends(get_db),
                              current_user: User = Depends(get_current_user)):
    if current_user.user_type != UserTypeEnum.professional:
        raise HTTPException(status_code=403, detail="Apenas disponível para a psicóloga")

    today = date.today()

    appointment = db.query(Appointment).filter(Appointment.patient_id == current_user.id,
        Appointment.date_time >= datetime.combine(datetime.now(), datetime.min.time()),
        Appointment.date_time <= datetime.combine(datetime.now(), datetime.max.time()),
        Appointment.status == 'confirmed'
        ).all()


    if not appointment:
        raise HTTPException(status_code=404, detail="Nenhum agendamento encontrado para hoje")

        return appointment
