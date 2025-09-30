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
        self.db_server_name = os.environ.get("MYSQL_DB_NAME", "ChangeMe123!")

    def _run_az_cmd(self, cmd: list):
        try:
            run(cmd, check=True)
        except CalledProcessError as e:
            print(f"[AzureDBCloudProvider] Command failed: {' '.join(cmd)}")
            raise e

    @override
    def get_cmd_create_database(self) -> str:
        """Create an Azure MySQL Flexible Server and database."""
        print(
            f"[AzureDBCloudProvider] Creating MySQL Flexible Server {self.db_server_name}..."
        )

        # Step 1: Create the MySQL Flexible Server if it doesn't exist
        cmd_server = [
            "az",
            "mysql",
            "flexible-server",  # <-- Changed from 'postgres server'
            "create",
            "--name",
            self.db_server_name,
            "--resource-group",
            self.resource_group,
            "--location",
            self.location,
            "--admin-user",
            self.admin_user,
            "--admin-password",
            self.admin_password,
            "--sku-name",
            "Standard_B1ms",  # <-- Changed SKU example for Flexible Server
            "--version",
            "8.0.21",  # <-- Changed version example for MySQL
            "--storage-size",
            "20",  # Flexible Server often requires this parameter
            "--tier",
            "Burstable",  # Flexible Server requires a tier argument
            "--public-access",
            "0.0.0.0",  # Example for no public access / VNET integration
        ]
        self._run_az_cmd(cmd_server)
        print(
            f"[AzureDBCloudProvider] MySQL Flexible Server {self.db_server_name} created. Creating database..."
        )

        # Step 2: Create the actual database on the Flexible Server
        cmd_db = [
            "az",
            "mysql",
            "flexible-server",
            "db",  # <-- Changed from 'postgres db'
            "create",
            "--database-name",  # <-- Changed argument name for database name
            self.db_server_name,
            "--server-name",
            self.db_server_name,
            "--resource-group",
            self.resource_group,
        ]
        self._run_az_cmd(cmd_db)

        return "MySQL Flexible Server and Database creation commands executed."

    @override
    def get_cmd_run_migrations(self) -> str:
        """Run migrations - this could be calling Alembic, Flyway, etc."""
        connection_string = self.get_connection_string()
        print(f"[AzureDBCloudProvider] Running migrations on {self.db_server_name}...")
        # Example: call Alembic or other migration tool here
        # subprocess.run(["alembic", "upgrade", "head", "-x", f"db_url={connection_string}"], check=True)

    @override
    def get_cmd_delete_database(self) -> str:
        server_name = self.db_server_name
        print(
            f"[AzureDBCloudProvider] Deleting DB {self.db_server_name} from server {server_name}..."
        )
        cmd = [
            "az",
            "postgres",
            "db",
            "delete",
            "--name",
            self.db_server_name,
            "--server-name",
            server_name,
            "--resource-group",
            self.resource_group,
            "--yes",
        ]
        self._run_az_cmd(cmd)

    @override
    def get_connection_string(self) -> str:
        admin_specs_cloud_sql = {
            "dialect": "mysql",
            "db_api": "mysqlconnector",
            "user": self.admin_user,
            "pw": self.admin_password,
            "hostname": f"{self.db_server_name}.mysql.database.azure.com",
            "provider": "azure",
        }
        dialect = admin_specs_cloud_sql["dialect"]
        db_api = admin_specs_cloud_sql["db_api"]

        user = admin_specs_cloud_sql["user"]
        pw = admin_specs_cloud_sql["pw"]
        hostname = admin_specs_cloud_sql["hostname"]
        dbname = admin_specs_cloud_sql["dbname"]
        url = f"{user}:{pw}@{hostname}/{dbname}"
        return f"{dialect}+{db_api}://{url}"
