from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.user_crud import create_user
from app.database_app import SessionLocal
from app.models.models import User
from app.schemas.user import UserResponse, UserTypeEnum, UserCreate

router = APIRouter(prefix="/professional", tags=["professional"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[UserResponse])
def get_all_professionals(db: Session = Depends(get_db)):
    return db.query(User).filter(User.tipo_usuario == UserTypeEnum.professional).all()

@router.post("/add_patient", response_model=UserResponse)
def add_patient(patient: UserCreate, db: Session = Depends(get_db)):

    # checando se o email já é cadastrado:
    existing_user = db.query(User).filter(User.email == patient.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    patient.type = UserTypeEnum.patient
    return create_user(db, patient)


