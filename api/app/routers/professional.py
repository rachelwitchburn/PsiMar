from fastapi import APIRouter, Depends, HTTPException
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


@router.post("/login", response_model=UserResponse)
def login_professional(access_code: str, db: Session = Depends(get_db)):
    """
    Rota para autenticar o profissional e gerar um token JWT.
    """
    # Aqui você pode implementar a lógica para verificar o access_code
    # e retornar o usuário correspondente.

    # Exemplo fictício:
    professional = professional = (
        db.query(User)
        .filter(User.access_code == access_code, User.tipo_usuario == UserTypeEnum.professional)
        .first()
    )
    if not professional:
        raise HTTPException(status_code=401, detail="Código de acesso inválido")

    return professional


@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Rota exclusiva para administradores verem todos os usuários cadastrados. dá pra testar quem tá cadastrado
    """
    return db.query(User).all()


"""
@router.get("/", response_model=list[UserResponse])
def get_all_professionals(db: Session = Depends(get_db)):
    return db.query(User).filter().all()
"""



@router.post("/add_patient", response_model=UserResponse)
def add_patient(patient: UserCreate, db: Session = Depends(get_db)):

    # checando se o email já é cadastrado:
    existing_user = db.query(User).filter(User.email == patient.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    patient.type = UserTypeEnum.patient
    return create_user(db, patient)


