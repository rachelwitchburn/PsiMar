from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database_app import SessionLocal
from app.models.models import User, Patient
from app.schemas.patient import PatientCompleteRegistration
from app.schemas.user import UserResponse, UserTypeEnum

router = APIRouter(prefix="/patient", tags=["patient"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[UserResponse])
def get_all_patients(db: Session = Depends(get_db)):
    return db.query(User).filter(User.user_type == UserTypeEnum.patient).all()

@router.post("/patient_complete_registration", response_model=UserResponse)
def complete_registration(data: PatientCompleteRegistration, db: Session = Depends(get_db)):
    patient = db.query(User).filter(Patient.email == data.email).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    if patient.password:
        raise HTTPException(status_code=400, detail="Paciente já está registrado")

    patient.password = data.password
    db.commit()
    db.refresh(patient)
    return patient
