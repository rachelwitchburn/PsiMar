import os  # Importando o módulo 'os' para trabalhar com variáveis de ambiente

from dotenv import load_dotenv  # Importando a função 'load_dotenv' para carregar variáveis do arquivo .env
# Importando classes do SQLAlchemy para configuração do banco de dados
from sqlalchemy import create_engine  # Classes para criação de engine e definição de colunas/tabelas
from sqlalchemy.ext.declarative import declarative_base  # Base para declarar modelos de dados do SQLAlchemy
from sqlalchemy.orm import sessionmaker  # Função para criar a sessão de interação com o banco de dados

load_dotenv()  # Carrega as variáveis do arquivo .env para o ambiente

# URL de conexão com o banco de dados (aqui usando SQLite local)
# A URL de conexão do banco é obtida da variável de ambiente DATABASE_URL, ou "sqlite:///default.db" por padrão.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")

# Criação do engine de conexão com o banco de dados
# 'check_same_thread': False é necessário para permitir múltiplas conexões com SQLite em threads diferentes.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Criando a sessão para interagir com o banco de dados
# 'autocommit' e 'autoflush' estão configurados como False para controlar explicitamente o comportamento das transações.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir as tabelas no banco de dados
# Usamos 'Base' como classe base para definir todas as tabelas do banco.
Base = declarative_base()


# Função para criar todas as tabelas definidas pelo SQLAlchemy
# Esta função cria todas as tabelas que foram definidas utilizando o modelo Base.
def create_tables():
    Base.metadata.create_all(bind=engine)  # Gera as tabelas no banco a partir da base definida, associada ao engine
