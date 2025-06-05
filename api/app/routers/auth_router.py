from datetime import timedelta
import os
from api.app.schemas.auth import LoginData, ResetPassword, TokenResponse
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from api.app.database_app import get_db
from api.app.models.models import User
from api.app.security import create_access_token, verify_password, get_current_user, decode_jwt_token, create_reset_token
from api.app.utils.email_utils import send_email
from api.app.schemas.auth import ResetPasswordWithToken, ForgotPasswordRequest
router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 60
RESET_TOKEN_EXPIRE_MINUTES = 30


@router.post("/login", response_model=TokenResponse, summary="Autenticar usuário")
async def login(credentials: LoginData, db: Session = Depends(get_db)):
    """
    Autentica um usuário e retorna um token JWT para acesso autorizado.

    - **email**: E-mail do usuário.
    - **password**: Senha do usuário.
    """
    try:
        user = db.query(User).filter(User.email == credentials.email).first()
    except Exception as e:
        print(f"[ERRO] Falha ao acessar o banco no login: {e}")
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados")

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

    return TokenResponse(access_token=access_token, token_type="bearer",user_type=user.user_type, user_id=user.id)

@router.post("/reset-password", summary="Redefinir senha do usuário autenticado")
async def reset_password(data: ResetPassword, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Permite que um usuário autenticado redefina sua senha.

    - **nova_senha**: Nova senha a ser definida.
    """
    current_user.password = pwd_context.hash(data.nova_senha)
    db.commit()
    return {"message": "Senha alterada com sucesso"}


@router.post("/forgot-password", summary="Solicitar redefinição de senha")
async def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    token = create_reset_token(
        email=str(user.email),
        expires_delta=timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    )

    reset_link = f"{os.getenv('FRONTEND_URL', 'http://127.0.0.1:8000')}/reset-password?token={token}"

    await send_email(
        to_email=str(user.email),
        subject="Recuperação de senha",
        content=(
            f"Olá {user.first_name},\n\n"
            f"Acesse o link para redefinir sua senha: {reset_link}\n\n"
            "Se não foi você, ignore este e-mail."
        )
    )

    return {"msg": "Se o e-mail estiver cadastrado, enviamos instruções para redefinir a senha."}


@router.post("/reset-password-with-token", summary="Redefinir senha via token de reset")
async def reset_password_with_token(
    data: ResetPasswordWithToken,
    db: Session = Depends(get_db)
):
    payload = decode_jwt_token(data.token)
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=400, detail="Token inválido")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.password = pwd_context.hash(data.nova_senha)
    db.commit()

    return {"message": "Senha redefinida com sucesso"}