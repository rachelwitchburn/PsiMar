from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.app.crud.login_service import authenticate_professional
from api.app.crud.user_crud import create_user
from api.app.database_app import get_db
from api.app.models.models import User
from api.app.schemas.user import UserResponse, UserTypeEnum, UserCreate
from api.app.security import get_current_user

router = APIRouter(prefix="/professional", tags=["professional"])

@router.post("/login", response_model=UserResponse)
async def login_professional(access_code: str, db: Session = Depends(get_db)):
    """
    Rota para autenticar o profissional via código de acesso.
    Chama o serviço de login que verifica as tentativas e o bloqueio de acesso.
    """
    return authenticate_professional(access_code, db)


@router.get("/", response_model=list[UserResponse])
async def get_all_users(db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    """
    Rota exclusiva para administradores verem todos os usuários cadastrados. dá pra testar quem tá cadastrado
    """
    if current_user.user_type != UserTypeEnum.professional:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    return db.query(User).all()


@router.post("/add_patient", response_model=UserResponse)
async def add_patient(patient: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
       Permite a profissionais adicionarem pacientes ao sistema.
    """

    if current_user.user_type != UserTypeEnum.professional:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Apenas profissionais podem adicionar pacientes.")

    existing_user = db.query(User).filter(User.email == patient.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    patient.user_type = UserTypeEnum.patient
    return create_user(db, patient)


