from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.app.crud.login_service import authenticate_professional
from api.app.crud import professional_service
from api.app.database_app import get_db
from api.app.models.models import User
from api.app.schemas.user import UserResponse, UserTypeEnum, UserCreate
from api.app.security import get_current_user
from api.app.schemas.professional import ProfessionalOut
from typing import List

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
    Rota exclusiva para profissionais verem todos os usuários cadastrados. dá pra testar quem tá cadastrado
    """
    if current_user.user_type != UserTypeEnum.professional:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    return db.query(User).all()


@router.get("/list", response_model=List[ProfessionalOut])
async def list_professionals(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.user_type != UserTypeEnum.patient:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas pacientes podem listar profissionais."
        )

    professionals = professional_service.get_all_professionals(db)
    return professionals

