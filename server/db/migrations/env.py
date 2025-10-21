# Standard Python imports
import os
import sys
from typing import Optional
from dotenv import load_dotenv

# Alembic imports
from alembic import context

# SQLAlchemy imports
from sqlalchemy import engine_from_config
from sqlalchemy import pool


# --- CRITICAL PATH FIX ---
# Add the project's root directory to the system path.
# Since env.py is at server/db/migrations/, we go up three levels ('..', '..', '..')
# to ensure we can correctly import 'server.db.Schema'.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from db.migrations.db_connection import DB_Connection

load_dotenv("db/migrations/")
# --- 1. Import Model Definitions (The Desired State) ---
# Import the Base class which contains the Metadata for all ORM models.
try:
    # Use the fully qualified path to your schema definitions
    from db.Schema import Base

    target_metadata = Base.metadata
except ImportError:
    print(
        "FATAL ERROR: Could not import 'Base' from 'server.db.Schema'. Check PYTHONPATH."
    )
    # Set to None to allow the script to fail gracefully during initialization if models aren't ready
    target_metadata = None

# --- 2. Configuration Setup ---

# This retrieves the configuration section from alembic.ini (e.g., [alembic])
config = context.config

# Interpret the config file for Python's logging.
# --- FIX FOR KEYERROR: 'formatters' ---
# We are commenting out the logging config read to bypass the fragile
# configparser issue, while still getting the configuration options.
# fileConfig(config.config_file_name) # THIS LINE WAS REMOVED/COMMENTED OUT

# Get database URL from environment variable (CRITICAL FOR DEPLOYMENT)
# The deployer script will set DB_URL to the correct cloud connection string.
db_connection = DB_Connection()
DB_URL: Optional[str] = db_connection.get_connection_str()

if DB_URL:
    # If the URL is found, override the 'sqlalchemy.url' in the Alembic configuration
    config.set_main_option("sqlalchemy.url", DB_URL)
else:
    # Fallback to the setting in alembic.ini if not running in the deployment environment
    print(
        "WARNING: DB_URL environment variable not found. Using connection string from alembic.ini."
    )

# --- 3. Migration Functions ---


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This generates the SQL script without connecting to the actual DB.
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
    """Run migrations in 'online' mode."""
    # ...
    # CRITICAL: Add the connect_args dictionary to enforce SSL on Azure/Cloud SQL
    # Azure PostgreSQL often requires sslmode='require'
    # TODO: fix for mysql instead of postgres
    # connect_args = {"sslmode": "require"}
    connect_args = {}

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        # PASS THE SSL ARGUMENTS HERE
        connect_args=connect_args,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # include_schemas=True, # Uncomment if using schemas
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
