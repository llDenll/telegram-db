import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from models.base import metadata

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

section = config.config_ini_section
config.set_section_option(section, 'POSTGRES_DB', os.environ.get('POSTGRES_DB', 'postgres'))
config.set_section_option(section, 'POSTGRES_HOST', os.environ.get('POSTGRES_HOST', 'postgres'))
config.set_section_option(section, 'POSTGRES_PASSWORD', os.environ.get('POSTGRES_PASSWORD', 'postgres'))
config.set_section_option(section, 'POSTGRES_PORT', os.environ.get('POSTGRES_PORT', '5432'))
config.set_section_option(section, 'POSTGRES_USER', os.environ.get('POSTGRES_USER', 'postgres'))

target_metadata = metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
