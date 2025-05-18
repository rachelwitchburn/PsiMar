from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database_app import \
    SessionLocal
from app.models.models import User
from app.security import create_access_token, verify_password, \
    get_current_user

router = APIRouter(prefix="/auth",
                   tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



ACCESS_TOKEN_EXPIRE_MINUTES = 60



@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    """
    Rota para autenticar o usuário e gerar um token JWT.
    """

    usuario = db.query(User).filter(User.email == email).first()

    if not usuario or not verify_password(senha, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": usuario.email, "is_admin": usuario.is_admin},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": "professional" if usuario.is_admin else "patient"
    }




@router.post("/reset-password")
def reset_password(nova_senha: str, current_usuario: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    """
    Rota para usuários autenticados redefinirem sua própria senha.
    """

    current_usuario.password = pwd_context.hash(nova_senha)
    db.commit()

    return {"message": "Senha alterada com sucesso"}
