from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from api.app.models.models import Patient, User
from api.app.schemas.user import UserCreate
from api.app.security import get_password_hash  # Função que aplica hash na senha


def complete_patient_registration(db: Session, user_data: UserCreate):
    user: Optional[User] = db.query(User).filter_by(email=user_data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Email not pre-registered")

    if user.password:
        raise HTTPException(status_code=400, detail="User already registered")

    user.password = get_password_hash(user_data.password)
    user.user_type = user_data.user_type

    patient = Patient(id=user.id)
    db.add(patient)
    db.commit()
    db.refresh(user)

    return user

def get_all_patients(db: Session) -> List[dict]:
    patients = db.query(User).filter(User.user_type == 'patient').all()
    return [{"id": p.id, "name": f"{p.first_name} {p.last_name}"} for p in patients]