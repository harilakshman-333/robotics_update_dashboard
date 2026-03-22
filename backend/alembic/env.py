import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine
from backend.models import feed_item


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Use DATABASE_URL_PSYNC (psycopg2) for Alembic if present, else fallback to DATABASE_URL
database_url_psync = os.environ.get("DATABASE_URL_PSYNC")
database_url = os.environ.get("DATABASE_URL")
if database_url_psync:
    print(f"[alembic.env.py] Using DATABASE_URL_PSYNC for migrations: {database_url_psync}")
    config.set_main_option("sqlalchemy.url", database_url_psync)
elif database_url:
    print(f"[alembic.env.py] Using DATABASE_URL for migrations: {database_url}")
    config.set_main_option("sqlalchemy.url", database_url)
else:
    print(f"[alembic.env.py] WARNING: No database URL found in environment!")
    print(f"[alembic.env.py] sqlalchemy.url from config: {config.get_main_option('sqlalchemy.url')}")

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

target_metadata = feed_item.Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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
