from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.app.crud.user_service import create_user
from api.app.database_app import get_db
from api.app.models.models import User, LoginAttempt
from api.app.schemas.user import UserCreate, UserResponse
from api.app.security import get_current_user, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from api.app.schemas.auth import Token

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Rota para criar um novo usuário (paciente ou psicologo).
    """

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    return create_user(db, user)


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Rota para usuários autenticados verem seu próprio perfil.
    """
    return current_user


@router.get("/", response_model=list[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    """
    Rota exclusiva para administradores verem todos os usuários cadastrados.
    """
    return db.query(User).all()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Rota para autenticar o usuário e gerar um token JWT.
    Implementa bloqueio de 30 minutos após 5 tentativas de login falhas consecutivas.
    """
    email = form_data.username
    password = form_data.password

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    login_attempt = db.query(LoginAttempt).filter(LoginAttempt.user_id == user.id).first()

    if login_attempt:
        if login_attempt.lock_until and login_attempt.lock_until > datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Conta bloqueada. Tente novamente após {login_attempt.lock_until}.",
            )
        elif login_attempt.failed_attempts >= 5:

            login_attempt.lock_until = datetime.now(timezone.utc) + timedelta(minutes=30)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Muitas tentativas falhas. Sua conta foi bloqueada por 30 minutos.",
            )

    if not verify_password(password, user.password):

        if not login_attempt:
            login_attempt = LoginAttempt(user_id=user.__dict__['id'])
            db.add(login_attempt)

        login_attempt.failed_attempts += 1
        login_attempt.last_failed_attempt = datetime.now(timezone.utc)
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}