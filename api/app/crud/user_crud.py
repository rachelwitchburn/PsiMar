from fastapi import HTTPException  # Corrigido o import do HTTPException

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.models import User, Patient, Professional, AccessCode
from app.schemas.user import UserCreate, UserTypeEnum
from app.security import get_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserCreate):
    user_exists = db.query(User).filter_by(email=user.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_password = pwd_context.hash(user.password)

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password,
        user_type=user.user_type
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    if user.user_type == UserTypeEnum.professional:
        code = db.query(AccessCode).filter_by(code=user.access_code).first()
        if not code or code.used:
            raise HTTPException(status_code=400, detail="Invalid or already used access code.")
        professional = Professional(
            id=db_user.id,
            access_code=user.access_code
        )
        db.add(professional)
        code.used = True

    elif user.user_type == UserTypeEnum.patient:
        pre_registered_user = db.query(User).filter_by(email=user.email).first()
        if not pre_registered_user or pre_registered_user.password:
            raise HTTPException(status_code=400, detail="Patient not pre-registered or already registered.")
        patient = Patient(
            id=db_user.id,
        )
        db.add(patient)

    db.commit()
    return db_user
