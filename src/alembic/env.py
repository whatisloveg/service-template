from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Alembic config
alembic_config = context.config

# Настройки приложения
from app.core.settings import config as app_config
from app.db.base_class import Base
from app.models import *

# Логирование
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# Метаданные моделей
target_metadata = Base.metadata

# Подставляем sync URL из твоего Settings
alembic_config.set_main_option(
    "sqlalchemy.url", app_config.db_cfg.sqlalchemy_sync_database_uri
)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
