# Standard Python imports
import os
import sys
from logging.config import fileConfig

# Alembic imports
from alembic import context

# SQLAlchemy imports
from sqlalchemy import engine_from_config
from sqlalchemy import pool

# Add the 'server' root directory to the system path so we can import 'server.db.models'
# This is crucial when running Alembic commands from the 'server/' directory.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# --- 1. Import Model Definitions (The Desired State) ---
# Import the Base class which contains the Metadata for all ORM models.
# This tells Alembic what the desired final state of the database schema should be.
try:
    from server.db.models import Base

    target_metadata = Base.metadata
except ImportError:
    print(
        "FATAL ERROR: Could not import 'Base' from 'server.db.models'. Check PYTHONPATH."
    )
    target_metadata = None  # Set to None to allow the script to fail gracefully

# --- 2. Configuration Setup ---

# This retrieves the configuration section from alembic.ini (e.g., [alembic])
config = context.config

# Interpret the config file for Python's logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get database URL from environment variable (CRITICAL FOR DEPLOYMENT)
# The deployment scripts will set DB_URL to the correct cloud connection string.
DB_URL = os.environ.get("DB_URL")
if DB_URL:
    # If the URL is found, override the 'sqlalchemy.url' in the Alembic configuration
    # This ensures we use the correct live or test database.
    config.set_main_option("sqlalchemy.url", DB_URL)
else:
    # Fallback to the setting in alembic.ini if not running in the deployment environment
    print(
        "WARNING: DB_URL environment variable not found. Using connection string from alembic.ini."
    )


# --- 3. Migration Functions ---


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This essentially generates the SQL script without connecting to the actual DB.
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

    This connects to the database to run upgrades and check for changes (autogenerate).
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Schema comparison options (e.g., ignore tables/columns)
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
