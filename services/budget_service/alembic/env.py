from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.core.database import Base
from app.models.budget import Budget, BudgetItem  # Import all models here
import os
from dotenv import load_dotenv
import re

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# Fonte de verdade da URL do banco para o Alembic
# 1) Se ALEMBIC_DATABASE_URL estiver definida, usa diretamente
# 2) Caso exista apenas DATABASE_URL com driver async, converte para driver sync
# 3) Se nenhuma estiver definida, usa placeholders do alembic.ini com defaults locais
section = config.config_ini_section

# Load environment variables from local files if present
load_dotenv(".env.local")
load_dotenv()

# Defaults locais compatíveis com ambiente Mac sem Docker
default_user = os.getenv("POSTGRES_USER", "crm_user")
default_password = os.getenv("POSTGRES_PASSWORD", "crm_strong_password_2024")
default_host = os.getenv("POSTGRES_HOST", "localhost")
default_port = os.getenv("POSTGRES_PORT", "5432")
default_db = os.getenv("POSTGRES_DB", "crm_ditual")

# Definir defaults no ini (serão usados se não houver URL explícita)
config.set_section_option(section, "POSTGRES_USER", default_user)
config.set_section_option(section, "POSTGRES_PASSWORD", default_password)
config.set_section_option(section, "POSTGRES_HOST", default_host)
config.set_section_option(section, "POSTGRES_PORT", default_port)
config.set_section_option(section, "POSTGRES_DB", default_db)

# Tentar obter URL explícita do ambiente
alembic_url = os.getenv("ALEMBIC_DATABASE_URL")
if not alembic_url:
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        # Converter driver async para sync, caso necessário
        if db_url.startswith("postgresql+asyncpg://"):
            alembic_url = db_url.replace("postgresql+asyncpg://", "postgresql://", 1)
        else:
            alembic_url = db_url

if alembic_url:
    # Sobrescrever sqlalchemy.url para o Alembic usar a URL explícita
    config.set_main_option("sqlalchemy.url", alembic_url)

# Log sanitized sqlalchemy.url for diagnostics
effective_url = config.get_main_option("sqlalchemy.url")
if effective_url:
    try:
        sanitized_url = re.sub(r":([^@]+)@", ":*****@", effective_url)
    except Exception:
        sanitized_url = effective_url
    print(f"Alembic usando sqlalchemy.url: {sanitized_url}")

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
