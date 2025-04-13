from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.user_crud import create_user
from app.database_app import SessionLocal
from app.models.models import User, LoginAttempt
from app.schemas.user import UserCreate, UserResponse
from app.security import get_current_user, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserResponse)
def register_user(usuario: UserCreate, db: Session = Depends(get_db)):
    """
    Rota para criar um novo usuário (paciente ou psicologo).
    """

    existing_usuario = db.query(User).filter(User.email == usuario.email).first()
    if existing_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    return create_user(db, usuario)


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Rota para usuários autenticados verem seu próprio perfil.
    """
    return current_user


@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Rota exclusiva para administradores verem todos os usuários cadastrados.
    """
    return db.query(User).all()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    """
    Rota para autenticar o usuário e gerar um token JWT.
    Implementa bloqueio de 30 minutos após 5 tentativas de login falhas consecutivas.
    """

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    login_attempt = db.query(LoginAttempt).filter(LoginAttempt.usuario_id == user.id).first()

    if login_attempt:

        if login_attempt.lock_until and login_attempt.lock_until > datetime.utcnow():

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Conta bloqueada. Tente novamente após {login_attempt.lock_until}.",
            )
        elif login_attempt.failed_attempts >= 5:

            login_attempt.lock_until = datetime.utcnow() + timedelta(minutes=30)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Muitas tentativas falhas. Sua conta foi bloqueada por 30 minutos.",
            )

    if not verify_password(senha, user.password):

        if not login_attempt:
            login_attempt = LoginAttempt(usuario_id=user.id)
            db.add(login_attempt)

        login_attempt.failed_attempts += 1
        login_attempt.last_failed_attempt = datetime.utcnow()
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
"""
    if login_attempt:
        login_attempt.failed_attempts = 0
        login_attempt.lock_until = None
        db.commit()

    # access_token = create_access_token(data={"sub": user.email, "is_admin": user.is_admin}) NÃO TEM IS_ADMIN MAIS

    return {"access_token": access_token, "token_type": "bearer"}
"""