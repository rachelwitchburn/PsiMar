from datetime import datetime, time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.app.database_app import get_db
from api.app.models.models import User, UserTypeEnum, Appointment
from api.app.security import get_current_user
from api.app.schemas.appointment import ViewAppointment

router = APIRouter(prefix="/schedule", tags=["Schedule"])

@router.get("/today", response_model=list[ViewAppointment], summary="Agenda diária da psicóloga")
async def get_professional_schedule(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
       Retorna os agendamentos confirmados de hoje para o profissional autenticado.
    """
    if current_user.user_type != UserTypeEnum.professional:
        raise HTTPException(status_code=403, detail="Apenas disponível para a psicóloga")

    today = datetime.today().date()

    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    appointment = db.query(Appointment).filter(Appointment.patient_id == current_user.id,
        Appointment.date_time >= start_of_day,
        Appointment.date_time <= end_of_day,
        Appointment.status == 'confirmed'
        ).all()


    if not appointment:
        raise HTTPException(status_code=404, detail="Nenhum agendamento encontrado para hoje")

    return appointment
