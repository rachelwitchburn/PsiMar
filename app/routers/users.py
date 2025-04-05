# Importando os módulos necessários
from fastapi import APIRouter, Depends, HTTPException, status   # FastAPI para criar rotas e lançar exceções
from sqlalchemy.orm import Session  # Para interagir com o banco de dados usando SQLAlchemy
from app.database_app import SessionLocal  # Para obter uma instância de sessão de banco de dados
from app.models import Usuario, LoginAttempt  # O modelo do usuário e tentativas de login no banco de dados
from app.schemas import UsuarioCreate, UsuarioResponse  # Schemas Pydantic para validação e formatação dos dados
from app.crud import create_user  # Função para criação de um novo usuário (geralmente no arquivo `crud.py`)
from app.security import get_current_usuario, is_admin, verify_password, create_access_token  # Funções para autenticação, verificação de senha e geração de tokens
from datetime import datetime, timedelta  # Para lidar com datas e tempo (ex: bloqueio de login por 30 minutos)

# Definindo um roteador para gerenciar as rotas do usuário
router = APIRouter(prefix="/users", tags=["users"])  # Prefixo para a URL e a tag associada à documentação

# Função que cria a sessão de banco de dados para ser usada nas rotas
def get_db():
    db = SessionLocal()  # Cria uma nova sessão do banco de dados
    try:
        yield db  # Retorna a sessão para ser usada como dependência
    finally:
        db.close()  # Garante que a sessão será fechada quando terminar

# Rota POST para criar um novo usuário
@router.post("/", response_model=UsuarioResponse)  # Cria um novo usuário e retorna um modelo UserResponse
def register_user(usuario: UsuarioCreate, db: Session = Depends(get_db)):  # Recebe o usuário para criação e uma sessão de banco de dados
    """
    Rota para criar um novo usuário (paciente ou administrador).
    """
    # Verifica se o usuário aceitou os termos de uso antes de permitir o cadastro
    if not usuario.aceitou_termos:
        raise HTTPException(status_code=400, detail="Os termos devem ser aceitos para cadastro.")

    # Verifica se já existe um usuário com o mesmo email no banco de dados
    existing_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existing_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")  # Se encontrar, lança uma exceção HTTP 400

    # Chama a função create_user para criar o usuário no banco de dados
    return create_user(db, usuario)  # Cria o usuário e retorna a resposta com os dados do usuário

# Rota GET para obter o perfil do usuário autenticado
@router.get("/me", response_model=UsuarioResponse)  # Obtém o perfil do usuário e retorna um modelo UserResponse
def get_my_profile(current_user: Usuario = Depends(get_current_usuario)):  # Obtém o usuário autenticado através do token JWT
    """
    Rota para usuários autenticados verem seu próprio perfil.
    """
    return current_user  # Retorna o usuário autenticado

# Rota GET para obter todos os usuários (restrita a administradores)
@router.get("/", dependencies=[Depends(is_admin)])  # Exige que o usuário seja um administrador para acessar
def get_all_users(db: Session = Depends(get_db)):  # Obtém todos os usuários no banco de dados
    """
    Rota exclusiva para administradores verem todos os usuários cadastrados.
    """
    return db.query(Usuario).all()  # Retorna todos os usuários da tabela User no banco de dados


def get_db():
    db = SessionLocal()  # Cria uma nova sessão do banco de dados
    try:
        yield db  # Retorna a sessão para ser usada como dependência
    finally:
        db.close()  # Garante que a sessão será fechada quando terminar


# Rota POST para login de usuário
@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):  # Recebe email, senha e a sessão do banco de dados
    """
    Rota para autenticar o usuário e gerar um token JWT.
    Implementa bloqueio de 30 minutos após 5 tentativas de login falhas consecutivas.
    """
    # Verificar se o usuário existe no banco de dados
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        # Se o usuário não for encontrado, retorna uma exceção HTTP 401 (não autorizado)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar o estado de bloqueio do usuário
    login_attempt = db.query(LoginAttempt).filter(LoginAttempt.usuario_id == usuario.id).first()

    if login_attempt:
        # Se o usuário tem uma tentativa de login registrada, verificar se está bloqueado
        if login_attempt.lock_until and login_attempt.lock_until > datetime.utcnow():
            # Se o bloqueio ainda estiver em vigor, retorna erro de conta bloqueada
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Conta bloqueada. Tente novamente após {login_attempt.lock_until}.",
            )
        elif login_attempt.failed_attempts >= 5:
            # Se o número de tentativas falhas for maior ou igual a 5, bloqueia a conta por 30 minutos
            login_attempt.lock_until = datetime.utcnow() + timedelta(minutes=30)
            db.commit()  # Confirma as mudanças no banco de dados
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Muitas tentativas falhas. Sua conta foi bloqueada por 30 minutos.",
            )

    # Verificar a senha fornecida
    if not verify_password(senha, usuario.senha):
        # Se a senha estiver errada, atualiza a contagem de tentativas falhas
        if not login_attempt:
            # Se ainda não houver uma tentativa de login registrada, cria uma nova
            login_attempt = LoginAttempt(usuario_id=usuario.id)
            db.add(login_attempt)  # Adiciona ao banco de dados

        # Incrementa o número de tentativas falhas e registra o momento da última falha
        login_attempt.failed_attempts += 1
        login_attempt.last_failed_attempt = datetime.utcnow()
        db.commit()  # Confirma as mudanças no banco de dados

        # Retorna um erro 401 (credenciais inválidas)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Se a senha for correta, resetar as tentativas falhas e desbloquear a conta, se necessário
    if login_attempt:
        login_attempt.failed_attempts = 0  # Reseta as tentativas falhas
        login_attempt.lock_until = None  # Remove qualquer bloqueio de tempo
        db.commit()  # Confirma as mudanças no banco de dados

    # Cria um token de acesso JWT para o usuário autenticado
    access_token = create_access_token(data={"sub": usuario.email, "is_admin": usuario.is_admin})

    # Retorna o token de acesso
    return {"access_token": access_token, "token_type": "bearer"}
