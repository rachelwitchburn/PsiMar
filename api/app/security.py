from datetime import datetime, timedelta  # Importando classes para trabalhar com datas e intervalos de tempo

from fastapi import Depends, HTTPException, \
    status  # Importando classes e funções do FastAPI para dependências e exceções
from fastapi.security import \
    OAuth2PasswordBearer  # Importando OAuth2PasswordBearer para lidar com autenticação baseada em OAuth2
from jose import JWTError, jwt  # Importando a biblioteca 'jose' para trabalhar com JWT (JSON Web Tokens)
from passlib.context import CryptContext  # Importando 'CryptContext' para trabalhar com criptografia de senhas
from sqlalchemy.orm import Session  # Importando Session do SQLAlchemy para interação com o banco de dados

from api.app.database_app import SessionLocal  # Importando a função SessionLocal, que cria uma sessão do banco de dados
from api.app.models import \
    Usuario  # Importando o modelo Usuario para interagir com a tabela 'Usuarios' no banco de dados

SECRET_KEY = "chave-secreta-muito-segura"  # Chave secreta usada para assinar os tokens JWT. Deve ser substituída por uma chave forte e segura
ALGORITHM = "HS256"  # Algoritmo de hash usado para assinar o JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Tempo de expiração do token de acesso (em minutos)

# Instanciando o contexto para criptografar senhas com bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Instanciando a dependência para OAuth2 com senha (será usada para o token de autenticação)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login")  # A URL de login será 'auth/login', onde o token será gerado


# Função para verificar se a senha fornecida (plain_password) é válida em relação à senha armazenada (hashed_password)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,
                              hashed_password)  # Verifica se a senha informada corresponde à senha criptografada


# Função para gerar o hash de uma senha fornecida
def get_password_hash(password):
    return pwd_context.hash(password)  # Cria um hash seguro da senha com bcrypt


# Função para criar um token de acesso JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()  # Faz uma cópia dos dados para adicionar a expiração
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=15))  # Define a data de expiração do token
    to_encode.update({"exp": expire})  # Adiciona a data de expiração ao payload do token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Gera o token JWT com os dados e a chave secreta


# Função para obter uma sessão de banco de dados
def get_db():
    db = SessionLocal()  # Cria uma nova sessão do banco de dados
    try:
        yield db  # Retorna a sessão para ser usada nas dependências
    finally:
        db.close()  # Fecha a sessão ao final do uso


# Função para obter o usuário atual a partir do token JWT
def get_current_usuario(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(  # Exceção a ser levantada se o token for inválido
        status_code=status.HTTP_401_UNAUTHORIZED,  # Código de status HTTP para não autorizado
        detail="Token inválido",  # Detalhe da exceção
        headers={"WWW-Authenticate": "Bearer"},  # Header de autenticação
    )
    try:
        # Decodifica o token JWT e obtém as informações do payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # Obtém o email do usuário do payload
        is_admin: bool = payload.get("is_admin")  # Obtém o status de administrador do payload
        if email is None:  # Verifica se o email não foi encontrado no token
            raise credentials_exception  # Levanta a exceção de credenciais inválidas
    except JWTError:  # Exceção gerada caso haja erro na decodificação do JWT
        raise credentials_exception  # Levanta a exceção de credenciais inválidas

    # Consulta o banco de dados para obter o usuário com o email informado no token
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if Usuario is None:  # Se o usuário não for encontrado no banco
        raise credentials_exception  # Levanta a exceção de credenciais inválidas

    return Usuario  # Retorna o usuário autenticado


# Função para verificar se o usuário é um administrador
def is_admin(current_Usuario: Usuario = Depends(
    get_current_usuario)):  # Dependência que verifica se o usuário atual é um administrador
    """ Verifica se o usuário logado é um administrador """
    if not current_Usuario.is_admin:  # Se o usuário não for administrador
        raise HTTPException(  # Levanta uma exceção de acesso proibido
            status_code=status.HTTP_403_FORBIDDEN,  # Código de status HTTP para acesso proibido
            detail="Apenas administradores podem acessar essa rota",  # Detalhe da exceção
        )
    return current_Usuario  # Retorna o usuário, se ele for administrador
