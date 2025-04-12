# Importa as bibliotecas necessárias
import os  # Para manipulação de variáveis de ambiente e caminhos
from dotenv import load_dotenv  # Para carregar variáveis de ambiente de um arquivo .env
from logging.config import fileConfig  # Para configurar o logging do Alembic
from sqlalchemy import engine_from_config  # Para criar o motor de conexão do SQLAlchemy
from sqlalchemy import pool  # Para gerenciar pools de conexões no SQLAlchemy
from alembic import context  # Contexto do Alembic para migrações
from api.app.models import Base  # Importa o modelo Base, que contém a metadata dos modelos de banco de dados


# Carrega as variáveis de ambiente do arquivo .env, se disponível
load_dotenv()

# Obtém a URL de conexão com o banco de dados a partir das variáveis de ambiente ou usa um valor padrão
url = os.getenv("DATABASE_URL", "sqlite:///default.db")  # A URL do banco de dados, ou "sqlite:///default.db" se não estiver definida

# Configuração do Alembic - prepara o arquivo de configuração do Alembic
config = context.config  # Carrega as configurações do Alembic

# Verifica se o arquivo de configuração de logging está presente e, em caso afirmativo, carrega-o
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define a metadata do modelo para que o Alembic possa usar a estrutura do banco de dados durante as migrações
target_metadata = Base.metadata  # A metadata contém informações sobre os modelos de dados no SQLAlchemy

def run_migrations_offline() -> None:
    """Executar migrações no modo 'offline'."""
    # Configura o contexto do Alembic para trabalhar offline (usando URL diretamente)
    context.configure(
        url=url,  # URL do banco de dados
        target_metadata=target_metadata,  # Metadata dos modelos do banco de dados
        literal_binds=True,  # Usa a ligação literal dos parâmetros (em vez de placeholders)
        dialect_opts={"paramstyle": "named"},  # Estilo de parâmetros nomeados para o banco de dados
    )

    # Inicia a transação e executa as migrações
    with context.begin_transaction():
        context.run_migrations()  # Executa as migrações

def run_migrations_online() -> None:
    """Executar migrações no modo 'online'."""
    # Cria uma conexão com o banco de dados a partir das configurações do Alembic
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),  # Obtém as configurações do banco de dados no arquivo de configuração
        prefix="sqlalchemy.",  # Prefixo para identificar as configurações do SQLAlchemy
        poolclass=pool.NullPool,  # Usar o NullPool para não gerenciar um pool de conexões (útil para migrações)
    )

    # Cria uma conexão com o banco de dados
    with connectable.connect() as connection:
        # Configura o contexto do Alembic para usar a conexão estabelecida
        context.configure(
            connection=connection,  # A conexão com o banco de dados
            target_metadata=target_metadata  # A metadata dos modelos de dados
        )

        # Inicia a transação e executa as migrações
        with context.begin_transaction():
            context.run_migrations()  # Executa as migrações

# Verifica se o Alembic está no modo offline (usando URL diretamente) ou online (usando conexão real com o banco)
if context.is_offline_mode():
    run_migrations_offline()  # Se estiver offline, executa migrações offline
else:
    run_migrations_online()  # Se estiver online, executa migrações online