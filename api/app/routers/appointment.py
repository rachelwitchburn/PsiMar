from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database_app import get_db
from app.schemas.appointment import CreateAppointment

router = APIRouter(prefix="/appointment", tags=["appointment"])

@router.get("/", response_model=list[schemas.Appointment])
def get_appointments(db: Session = Depends(get_db), professional_id: int = 1):
    appointments = crud.appointment_list(db=db, professional_id=professional_id)
    if not appointments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum agendamento encontrado.")
    return appointments

@router.post("/create", response_model=schemas.Appointment)
def create_appointment(appointment: CreateAppointment, db: Session = Depends(get_db), professional_id: int = 1):
    return crud.create_appointment(db=db, appointment=appointment, professional_id=professional_id)

@router.post("/confirm/{appointment_id}", response_model=schemas.Appointment)
def confirm_appointment(appointment_id: int, db: Session = Depends(get_db), patient_id: int = 1):
    appointment = crud.confirm_appointment(db=db, appointment_id=appointment_id, patient_id=patient_id)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento não encontrado.")
    return appointment

