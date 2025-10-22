# Standard Python imports
import os
import sys
from dotenv import load_dotenv

# Alembic imports

# SQLAlchemy imports
from db.Schema import database_specs, database_specs_cloud_sql
from db.util.connections import construct_conn_str_any

# --- CRITICAL PATH FIX ---
# Add the project's root directory to the system path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

load_dotenv("db/migrations/")


class DB_Connection:
    def __init__(self):
        self.DEPLOYMENT = os.environ.get("DEPLOYMENT")
        if self.DEPLOYMENT == "local":
            self.DB_SPECS = database_specs
        else:
            self.DB_SPECS = database_specs_cloud_sql

        # New instance attribute for the safe URL
        self.safe_log_url = None
        # New instance attribute for only the hostname
        self.hostname_only = None

    def get_connection_str(self):
        full_url = construct_conn_str_any(self.DB_SPECS, self.DEPLOYMENT)

        # --- LOGGING LOGIC START ---

        try:
            # 1. Hide the credentials (everything between // and @)
            parts = full_url.split("@")
            host_and_db = (
                parts[1] if len(parts) > 1 else full_url
            )  # Everything after the @ (or the full URL)
            protocol_and_user = parts[0].split("//")

            # Reconstruct the URL showing only the host and database (for context)
            self.safe_log_url = f"{protocol_and_user[0]}://...@{host_and_db}"

            # 2. Extract the Hostname Only
            # The format is typically: <hostname>/<database>?...
            self.hostname_only = host_and_db.split("/")[0].split("?")[
                0
            ]  # Split by /, then by ? for parameters

        except Exception as e:
            self.safe_log_url = f"URL PARSING ERROR: {e}"
            self.hostname_only = f"HOSTNAME PARSING ERROR: {e}"

        # --- INSTANCE VERIFICATION PRINT (NEW) ---
        print("-" * 50)
        print(f"VERIFYING TARGET INSTANCE: {self.hostname_only}")
        print("-" * 50)
        # --- LOGGING LOGIC END ---

        return full_url
