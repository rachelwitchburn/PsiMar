# Importando a classe Column do SQLAlchemy e Base de database.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime  # Importando as classes necessárias do SQLAlchemy para definir as colunas e tipos de dados
from app.database import Base  # Importando a base de dados que contém a configuração do banco de dados (Base), geralmente usada para definir modelos
from datetime import datetime  # Importando a classe datetime para manipular datas e horas

# Definindo o modelo de dados "User" para a tabela "users"
class User(Base):  # Definindo a classe User, que herda de Base (geralmente a base é declarada como um modelo para o banco de dados)
    # Nome da tabela no banco de dados
    __tablename__ = "users"  # A tabela no banco de dados será chamada "users"

    # Definição das colunas da tabela
    id = Column(Integer, primary_key=True, index=True)  # Definindo a coluna 'id' como chave primária (integer) e com índice
    nome = Column(String, index=True)  # Definindo a coluna 'nome' como tipo string, e indexada para consultas rápidas
    email = Column(String, unique=True, index=True)  # Definindo a coluna 'email' como string, única (não pode haver e-mails repetidos) e indexada
    senha = Column(String)  # A coluna 'senha' armazena a senha do usuário como uma string
    is_admin = Column(Boolean, default=False)  # A coluna 'is_admin' define se o usuário é administrador (valor padrão é False)
    aceitou_termos = Column(Boolean, default=False)  # A coluna 'aceitou_termos' define se o usuário aceitou os termos de uso (valor padrão é False)

# Modelo de dados para registrar tentativas de login
class LoginAttempt(Base):  # Definindo a classe LoginAttempt para registrar as tentativas de login
    __tablename__ = "login_attempts"  # A tabela no banco de dados será chamada "login_attempts"

    id = Column(Integer, primary_key=True, index=True)  # Definindo a coluna 'id' como chave primária (integer) e com índice
    user_id = Column(Integer, index=True)  # A coluna 'user_id' armazena o ID do usuário relacionado à tentativa de login (indexada para consultas rápidas)
    failed_attempts = Column(Integer, default=0)  # A coluna 'failed_attempts' mantém o contador de tentativas falhas (valor padrão é 0)
    last_failed_attempt = Column(DateTime, default=datetime.utcnow)  # A coluna 'last_failed_attempt' registra o horário da última tentativa falha
    lock_until = Column(DateTime, nullable=True)  # A coluna 'lock_until' armazena a data e hora até a qual o usuário está bloqueado após falhas sucessivas (nullable, ou seja, pode ser nulo)
