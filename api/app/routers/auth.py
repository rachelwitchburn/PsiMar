from datetime import timedelta  # Importando timedelta para definir o tempo de expiração do token

from fastapi import APIRouter, Depends, HTTPException, status  # Importando dependências do FastAPI
from passlib.context import CryptContext  # Importando CryptContext para trabalhar com a criptografia de senhas
from sqlalchemy.orm import Session  # Importando Session do SQLAlchemy para interagir com o banco de dados

from api.app.database_app import \
    SessionLocal  # Importando a função SessionLocal para obter uma sessão de banco de dados
from api.app.models import Usuario  # Importando o modelo Usuario para interagir com a tabela 'users' no banco de dados
from api.app.security import create_access_token, verify_password, \
    get_current_usuario  # Importando funções de segurança

router = APIRouter(prefix="/auth",
                   tags=["auth"])  # Definindo o roteador para autenticação com prefixo '/auth' e tag 'auth'

pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")  # Instanciando o contexto de criptografia de senha com bcrypt


# Função para obter uma sessão de banco de dados
def get_db():
    db = SessionLocal()  # Cria uma nova sessão do banco de dados
    try:
        yield db  # Retorna a sessão para ser usada nas dependências
    finally:
        db.close()  # Fecha a sessão quando terminar


# Configuração do tempo de expiração do token (60 minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Rota de login para autenticar o usuário e gerar um token JWT
@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    """
    Rota para autenticar o usuário e gerar um token JWT.
    """
    # Consulta o banco de dados para encontrar o usuário com o email fornecido
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    # Verifica se o usuário não existe ou se a senha fornecida não corresponde à senha armazenada
    if not usuario or not verify_password(senha, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # Código de erro de não autorizado
            detail="Credenciais inválidas",  # Detalhe da exceção
            headers={"WWW-Authenticate": "Bearer"},  # Instrução para autenticação com Bearer Token
        )

    # Configura o tempo de expiração do token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Gera o token de acesso JWT com os dados do usuário
    access_token = create_access_token(data={"sub": usuario.email, "is_admin": usuario.is_admin},
                                       expires_delta=access_token_expires)

    # Retorna o token de acesso no formato 'bearer'
    return {"access_token": access_token, "token_type": "bearer"}


# Rota para redefinir a senha do usuário autenticado
@router.post("/reset-password")
def reset_password(nova_senha: str, current_usuario: Usuario = Depends(get_current_usuario),
                   db: Session = Depends(get_db)):
    """
    Rota para usuários autenticados redefinirem sua própria senha.
    """
    # Criptografa a nova senha fornecida e a armazena no banco de dados
    current_usuario.senha = pwd_context.hash(nova_senha)
    db.commit()  # Commit para salvar a alteração no banco de dados
    # Retorna uma mensagem de sucesso
    return {"message": "Senha alterada com sucesso"}
