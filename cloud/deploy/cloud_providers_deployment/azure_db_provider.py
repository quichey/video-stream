import os
from subprocess import run, CalledProcessError
from .base_db_cloud_provider import BaseDBCloudProvider


class AzureDBCloudProvider(BaseDBCloudProvider):
    PROVIDER_NAME = "azure-db"

    def __init__(self, context, env):
        super().__init__(context, env)
        self.resource_group = os.environ.get("RESOURCE_GROUP_CENTRAL", "default-rg")
        self.location = os.environ.get("AZURE_LOCATION", "westus2")
        self.admin_user = os.environ.get("DB_ADMIN_USER", "admin")
        self.admin_password = os.environ.get("DB_ADMIN_PASSWORD", "ChangeMe123!")
        self.db_server_name_prefix = f"{context}-db"

    def _run_az_cmd(self, cmd: list):
        try:
            run(cmd, check=True)
        except CalledProcessError as e:
            print(f"[AzureDBCloudProvider] Command failed: {' '.join(cmd)}")
            raise e

    def create_database(self, db_name: str):
        """Create a Postgres database in Azure (example)."""
        server_name = f"{self.db_server_name_prefix}-{self.env}"
        print(f"[AzureDBCloudProvider] Creating DB server {server_name}...")

        # Step 1: Create the PostgreSQL server if it doesn't exist
        cmd_server = [
            "az",
            "postgres",
            "server",
            "create",
            "--name",
            server_name,
            "--resource-group",
            self.resource_group,
            "--location",
            self.location,
            "--admin-user",
            self.admin_user,
            "--admin-password",
            self.admin_password,
            "--sku-name",
            "B_Gen5_1",  # example
            "--version",
            "14",
        ]
        self._run_az_cmd(cmd_server)

        # Step 2: Create the actual database
        cmd_db = [
            "az",
            "postgres",
            "db",
            "create",
            "--name",
            db_name,
            "--server-name",
            server_name,
            "--resource-group",
            self.resource_group,
        ]
        self._run_az_cmd(cmd_db)

    def run_migrations(self, db_name: str):
        """Run migrations - this could be calling Alembic, Flyway, etc."""
        connection_string = self.get_connection_string(db_name)
        print(f"[AzureDBCloudProvider] Running migrations on {db_name}...")
        # Example: call Alembic or other migration tool here
        # subprocess.run(["alembic", "upgrade", "head", "-x", f"db_url={connection_string}"], check=True)

    def delete_database(self, db_name: str):
        server_name = f"{self.db_server_name_prefix}-{self.env}"
        print(
            f"[AzureDBCloudProvider] Deleting DB {db_name} from server {server_name}..."
        )
        cmd = [
            "az",
            "postgres",
            "db",
            "delete",
            "--name",
            db_name,
            "--server-name",
            server_name,
            "--resource-group",
            self.resource_group,
            "--yes",
        ]
        self._run_az_cmd(cmd)

    def get_connection_string(self, db_name: str) -> str:
        server_name = f"{self.db_server_name_prefix}-{self.env}"
        return f"postgresql://{self.admin_user}:{self.admin_password}@{server_name}.postgres.database.azure.com:5432/{db_name}"
