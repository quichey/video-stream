# Standard Python imports
import os
import sys

# Alembic imports

# SQLAlchemy imports
from db.Schema import database_specs, database_specs_cloud_sql
from db.util.connections import construct_conn_str_any

# --- CRITICAL PATH FIX ---
# Add the project's root directory to the system path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


class DB_Connection:
    def __init__(self):
        self.DEPLOYMENT = os.environ.get("DEPLOYMENT")
        if self.DEPLOYMENT == "local":
            self.DB_SPECS = database_specs
        else:
            self.DB_SPECS = database_specs_cloud_sql

        # New instance attribute for the safe URL
        self.safe_log_url = None

    def get_connection_str(self):
        full_url = construct_conn_str_any(self.DB_SPECS, self.DEPLOYMENT)

        # --- LOGGING LOGIC START ---

        # 1. Hide the credentials (everything between // and @)
        try:
            # Find the user:password part
            parts = full_url.split("@")
            host_and_db = (
                parts[1] if len(parts) > 1 else full_url
            )  # Fallback if @ isn't found
            protocol_and_user = parts[0].split("//")

            # Reconstruct the URL showing only the host and database
            safe_url = f"{protocol_and_user[0]}://...@{host_and_db}"

            self.safe_log_url = safe_url

        except Exception as e:
            # Fallback if URL parsing fails
            self.safe_log_url = f"URL PARSING ERROR: {e}"

        # --- LOGGING LOGIC END ---

        return full_url


# -------------------------------------------------------------
# You will now update run_migrations_online() in env.py (not shown here)
# to use the new safe_log_url attribute for logging:
# -------------------------------------------------------------

# Example of how you would use it in your env.py's run_migrations_online function:

"""
# Inside run_migrations_online:
db_conn = DB_Connection()
connectable_url = db_conn.get_connection_str()

# --- INSTANCE VERIFICATION LOGGING ---
context.py.print(f"--- MIGRATION TARGET: {db_conn.safe_log_url} ---")
# -------------------------------------

# Then, set the connection URL for Alembic
config.set_main_option("sqlalchemy.url", connectable_url)
# ... rest of the function ...
"""
