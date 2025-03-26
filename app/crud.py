# Importando a sessão do banco de dados e o modelo User
from sqlalchemy.orm import Session  # Importando a classe 'Session' para interagir com o banco de dados
from app.models import User  # Importando o modelo 'User', que representa a tabela de usuários no banco de dados

# Importando o esquema UserCreate para receber os dados de entrada
from app.schemas import \
    UserCreate  # Importando o esquema de validação 'UserCreate', usado para validar dados na criação de usuários

# Biblioteca para criptografar a senha
from passlib.context import CryptContext  # Importando a classe 'CryptContext' para lidar com criptografia de senhas

# Instanciando o contexto para criptografia de senhas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")  # Definindo o esquema de criptografia com bcrypt e indicando que esquemas antigos são depreciados


# Função para criar um novo usuário no banco de dados
def create_user(db: Session, user: UserCreate):
    # Criptografando a senha antes de salvar no banco
    hashed_password = pwd_context.hash(
        user.senha)  # Utilizando o 'pwd_context' para criptografar a senha fornecida pelo usuário

    # Criando uma instância do modelo User com os dados fornecidos
    db_user = User(
        nome=user.nome,  # Atribuindo o nome fornecido ao novo usuário
        email=user.email,  # Atribuindo o e-mail fornecido ao novo usuário
        senha=hashed_password,  # Atribuindo a senha criptografada ao novo usuário
        aceitou_termos=user.aceitou_termos  # Atribuindo o valor do campo 'aceitou_termos' ao novo usuário
    )

    db.add(db_user)  # Adicionando o novo usuário à sessão do banco de dados (não persistido ainda)
    db.commit()  # Comitando a sessão, ou seja, salvando a instância do usuário no banco de dados
    db.refresh(
        db_user)  # Atualizando o objeto db_user com os dados que foram persistidos no banco de dados (incluindo valores gerados automaticamente, como o ID)

    return db_user  # Retornando o usuário criado após a persistência no banco de dados
