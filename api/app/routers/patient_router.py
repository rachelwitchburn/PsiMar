from fastapi import HTTPException, status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.app.database_app import get_db
from api.app.models.models import User
from api.app.schemas.patient import PatientCompleteRegistration
from api.app.schemas.user import UserResponse, UserTypeEnum
from api.app.security import get_password_hash, get_current_user


router = APIRouter(prefix="/patient", tags=["patient"])

@router.get("/", response_model=list[UserResponse])
async def get_all_patients(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
      Retorna todos os pacientes cadastrados. Acesso restrito a profissionais e admins.
      """
    if current_user.user_type not in [UserTypeEnum.professional, UserTypeEnum.professional]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")

    return db.query(User).filter(User.user_type == UserTypeEnum.patient).all()

@router.post("/patient_complete_registration", response_model=UserResponse)
async def complete_registration(data: PatientCompleteRegistration, db: Session = Depends(get_db)):
    """
        Completa o cadastro de um paciente. Normalmente utilizado após cadastro inicial feito por um profissional.
    """
    patient = db.query(User).filter(User.email == data.email).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    if patient.password:
        raise HTTPException(status_code=400, detail="Paciente já está registrado")

    patient.password = get_password_hash(data.password)
    db.commit()
    db.refresh(patient)
    return patient

