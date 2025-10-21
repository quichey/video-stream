# Standard Python imports
import os
import sys

# Alembic imports

# SQLAlchemy imports
from db.Schema import database_specs, database_specs_cloud_sql
from db.util.connections import construct_conn_str_any

# --- CRITICAL PATH FIX ---
# Add the project's root directory to the system path.
# Since env.py is at server/db/migrations/, we go up three levels ('..', '..', '..')
# to ensure we can correctly import 'server.db.Schema'.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


class DB_Connection:
    def __init__(self):
        self.DEPLOYMENT = os.environ.get("DEPLOYMENT")
        if self.DEPLOYMENT == "local":
            self.DB_SPECS = database_specs
        else:
            self.DB_SPECS = database_specs_cloud_sql

    def get_connection_str(self):
        return construct_conn_str_any(self.DB_SPECS, self.DEPLOYMENT)
