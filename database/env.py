# Importa as bibliotecas necessárias
import os
from dotenv import load_dotenv
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from api.app.models.models import Base

# Carrega as variáveis de ambiente do arquivo .env, se disponível
load_dotenv()

# Caminho absoluto do banco
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, '..', 'api', 'app', 'build', 'database.sqlite')
db_file = os.path.abspath(db_file)

# Obtém a URL de conexão com o banco de dados a partir das variáveis de ambiente ou usa um valor padrão
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{db_file}")

# Alembic Config
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Verifica se o arquivo de configuração de logging está presente e, em caso afirmativo, carrega-o
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define a metadata do modelo para que o Alembic possa usar a estrutura do banco de dados durante as migrações
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Executar migrações no modo 'offline'."""

    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Inicia a transação e executa as migrações
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Executar migrações no modo 'online'."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Cria uma conexão com o banco de dados
    with connectable.connect() as connection:
        # Configura o contexto do Alembic para usar a conexão estabelecida
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        # Inicia a transação e executa as migrações
        with context.begin_transaction():
            context.run_migrations()

# Verifica se o Alembic está no modo offline (usando URL diretamente) ou online (usando conexão real com o banco)
if context.is_offline_mode():
    run_migrations_offline()  # Se estiver offline, executa migrações offline
else:
    run_migrations_online()  # Se estiver online, executa migrações online

