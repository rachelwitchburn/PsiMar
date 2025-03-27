# Importando a classe Column do SQLAlchemy e Base de database.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint  # Importando as classes necessárias do SQLAlchemy para definir as colunas e tipos de dados
from app.database import Base  # Importando a base de dados que contém a configuração do banco de dados (Base), geralmente usada para definir modelos
from datetime import datetime  # Importando a classe datetime para manipular datas e horas
from sqlalchemy.orm import relationship

# Definindo o modelo de dados "User" para a tabela "users"
class Usuario(Base):  # Definindo a classe User, que herda de Base (geralmente a base é declarada como um modelo para o banco de dados)
    # Nome da tabela no banco de dados
    __tablename__ = "Usuario"  # A tabela no banco de dados será chamada "Usuario"

    # Definição das colunas da tabela
    id = Column(Integer, primary_key=True, autoincrement=True)  # Definindo a coluna 'id' como chave primária (integer) e com índice
    nome = Column(String, nullable=False)  # Definindo a coluna 'nome' como tipo string, e indexada para consultas rápidas
    sobrenome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)  # Definindo a coluna 'email' como string, única (não pode haver e-mails repetidos) e indexada
    senha = Column(String, nullable=False)  # A coluna 'senha' armazena a senha do usuário como uma string
    tipo_usuario = Column(String, nullable=False)  
    aceitou_termos = Column(Boolean, default=False)  # A coluna 'aceitou_termos' define se o usuário aceitou os termos de uso (valor padrão é False)

    __table_args__ = (
        CheckConstraint(tipo_usuario.in_(['paciente', 'psicólogo']), name="tipo_usuario_check")
    )

class codigosAcesso(Base):
    __tablename__ = "codigosAcesso"
    codigo = Column(String, primary_key=True, unique=True)
    utilizado = Column(Boolean, default=False)

class Psicologo(Base):
    __tablename__ = "Psicologo"
    id = Column(Integer, ForeignKey("Usuario.id"), primary_key=True)
    codigosAcesso = Column(String, ForeignKey("codigosAcesso.codigo"), nullable=False)

    pacientes = relationship("Paciente", back_populates="psicologo")

class Paciente(Base):
    __tablename__ = "Paciente"
    id = Column(Integer, ForeignKey("Usuario.id"), primary_key=True)
    psicologo_id = Column(Integer, ForeignKey("Psicologo.id"), nullable=False)

    psicologo = relationship("Psicologo", back_populates="pacientes")

# Modelo de dados para registrar tentativas de login
class LoginAttempt(Base):  # Definindo a classe LoginAttempt para registrar as tentativas de login
    __tablename__ = "login_attempts"  # A tabela no banco de dados será chamada "login_attempts"

    id = Column(Integer, primary_key=True, index=True)  # Definindo a coluna 'id' como chave primária (integer) e com índice
    user_id = Column(Integer, index=True)  # A coluna 'user_id' armazena o ID do usuário relacionado à tentativa de login (indexada para consultas rápidas)
    failed_attempts = Column(Integer, default=0)  # A coluna 'failed_attempts' mantém o contador de tentativas falhas (valor padrão é 0)
    last_failed_attempt = Column(DateTime, default=datetime.utcnow)  # A coluna 'last_failed_attempt' registra o horário da última tentativa falha
    lock_until = Column(DateTime, nullable=True)  # A coluna 'lock_until' armazena a data e hora até a qual o usuário está bloqueado após falhas sucessivas (nullable, ou seja, pode ser nulo)
