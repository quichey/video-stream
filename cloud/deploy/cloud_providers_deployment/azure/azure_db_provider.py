import os
from typing_extensions import override
from subprocess import run, CalledProcessError
from cloud_providers_deployment.base.base_db_provider import BaseDBCloudProvider
from cloud_providers_deployment.azure.azure_base import AzureBaseProvider


class AzureDBCloudProvider(AzureBaseProvider, BaseDBCloudProvider):
    PROVIDER_NAME = "azure-db"

    def __init__(self, context, env):
        super().__init__(context, env)
        self.admin_user = os.environ.get("MYSQL_ADMIN_NAME", "admin")
        self.admin_password = os.environ.get("MYSQL_ADMIN_PW", "ChangeMe123!")
        self.db_server_name_prefix = os.environ.get("MYSQL_DB_NAME", "ChangeMe123!")

    def _run_az_cmd(self, cmd: list):
        try:
            run(cmd, check=True)
        except CalledProcessError as e:
            print(f"[AzureDBCloudProvider] Command failed: {' '.join(cmd)}")
            raise e

    @override
    def get_cmd_create_database(self) -> str:
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
            self.db_name,
            "--server-name",
            server_name,
            "--resource-group",
            self.resource_group,
        ]
        self._run_az_cmd(cmd_db)

    @override
    def get_cmd_run_migrations(self) -> str:
        """Run migrations - this could be calling Alembic, Flyway, etc."""
        connection_string = self.get_connection_string(self.db_name)
        print(f"[AzureDBCloudProvider] Running migrations on {self.db_name}...")
        # Example: call Alembic or other migration tool here
        # subprocess.run(["alembic", "upgrade", "head", "-x", f"db_url={connection_string}"], check=True)

    @override
    def get_cmd_delete_database(self) -> str:
        server_name = f"{self.db_server_name_prefix}-{self.env}"
        print(
            f"[AzureDBCloudProvider] Deleting DB {self.db_name} from server {server_name}..."
        )
        cmd = [
            "az",
            "postgres",
            "db",
            "delete",
            "--name",
            self.db_name,
            "--server-name",
            server_name,
            "--resource-group",
            self.resource_group,
            "--yes",
        ]
        self._run_az_cmd(cmd)

    @override
    def get_cmd_get_connection_string(self) -> str:
        server_name = f"{self.db_server_name_prefix}-{self.env}"
        return f"postgresql://{self.admin_user}:{self.admin_password}@{server_name}.postgres.database.azure.com:5432/{self.db_name}"
