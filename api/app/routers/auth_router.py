from datetime import timedelta
from api.app.schemas.auth import LoginData, ResetPassword, TokenResponse
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from api.app.database_app import get_db
from api.app.models.models import User
from api.app.security import create_access_token, verify_password, \
    get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 60



@router.post("/login", response_model=TokenResponse, summary="Autenticar usuário")
async def login(credentials: LoginData, db: Session = Depends(get_db)):
    """
    Autentica um usuário e retorna um token JWT para acesso autorizado.

    - **email**: E-mail do usuário.
    - **password**: Senha do usuário.
    """
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_type": user.user_type.value},
        expires_delta=access_token_expires
    )

    return TokenResponse(access_token=access_token, token_type="bearer")

@router.post("/reset-password", summary="Redefinir senha do usuário autenticado")
async def reset_password(data: ResetPassword, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Permite que um usuário autenticado redefina sua senha.

    - **nova_senha**: Nova senha a ser definida.
    """
    current_user.password = pwd_context.hash(data.nova_senha)
    db.commit()
    return {"message": "Senha alterada com sucesso"}
