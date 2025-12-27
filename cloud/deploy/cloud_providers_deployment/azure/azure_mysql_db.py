import os
from typing_extensions import override
from cloud_providers_deployment.azure.azure_db_provider import AzureDBProvider

# Note: AzureMySQLDBProvider no longer needs to import 'run' or 'CalledProcessError'
# because the execution logic is handled by the parent class's _run_az_cmd.


class AzureMySQLDBProvider(AzureDBProvider):
    # This class is concrete and implements the MySQL-Flexible-Server specifics
    PROVIDER_NAME = "azure-mysql-db"

    def __init__(self, context, env):
        super().__init__(context, env)

        # Define the necessary properties for the helpers to use
        self.admin_user = os.environ.get("MYSQL_ADMIN_NAME", "admin")
        self.admin_password = os.environ.get("MYSQL_ADMIN_PW", "ChangeMe123!")
        self.db_server_name = os.environ.get("MYSQL_DB_NAME", "ChangeMe123!")
        # Use a placeholder for the actual DB name if it differs from the server name
        self.database_name = os.environ.get("MYSQL_DB_NAME", "defaultdb")
        self.location = "us-west-2"

    # --- Implementation of Abstract Inner Helper Functions ---

    @override
    def _get_server_creation_command(self) -> list:
        """Returns the specific az command list for creating the MySQL Flexible Server."""
        print(
            f"[{self.PROVIDER_NAME}] Building MySQL Flexible Server creation command for {self.db_server_name}..."
        )
        return [
            "az",
            "mysql",
            "flexible-server",
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
            "Standard_B1ms",
            "--version",
            "8.0.21",
            "--storage-size",
            "20",
            "--tier",
            "Burstable",
            "--public-access",
            "0.0.0.0",  # VNET or 0.0.0.0 for all Azure services access
        ]

    @override
    def _get_db_creation_command(self) -> list:
        """Returns the specific az command list for creating the database on the server."""
        print(
            f"[{self.PROVIDER_NAME}] Building MySQL Database creation command for {self.database_name}..."
        )
        return [
            "az",
            "mysql",
            "flexible-server",
            "db",
            "create",
            "--database-name",
            self.database_name,
            "--server-name",
            self.db_server_name,
            "--resource-group",
            self.resource_group,
        ]

    @override
    def _get_server_deletion_command(self) -> list:
        """Returns the specific az command list for deleting the MySQL Flexible Server."""
        print(
            f"[{self.PROVIDER_NAME}] Building MySQL Flexible Server deletion command for {self.db_server_name}..."
        )
        return [
            "az",
            "mysql",
            "flexible-server",
            "delete",
            "--name",
            self.db_server_name,
            "--resource-group",
            self.resource_group,
            "--yes",
        ]

    @override
    def get_connection_details(self) -> dict:
        """Returns MySQL connection specifics."""
        return {
            "user": self.admin_user,
            "pw": self.admin_password,
            # Note: Azure Flexible Server requires user@serverName format for login
            "hostname": f"{self.db_server_name}.mysql.database.azure.com",
            "dbname": self.database_name,
        }

    @override
    def get_load_db_cmd(self, sql_file) -> str:
        """
        Returns a MySQL command to pipe the SQL file into the Azure database.
        Format: mysql -h <host> -u <user> -p<pass> <dbname> < <filename>
        """
        host = f"{self.db_server_name}.mysql.database.azure.com"

        # We return a list or string that the shell can execute.
        # Note: No space between -p and the password is standard for MySQL CLI.
        return (
            f"mysql -h {host} "
            f"-u {self.admin_user} "
            f"-p'{self.admin_password}' "
            f"{self.database_name} "
            f"< {sql_file}"
        )

    @override
    def get_cmd_provision_database_engine(self) -> list:
        """
        Returns Azure Flexible MySQL CLI command as a string for provisioning
        a new database engine instance on the server.
        """
        print(
            f"[{self.PROVIDER_NAME}] Generating CLI command to provisioning DB engine: {self.db_server_name}"
        )
        return [
            "az",
            "mysql",
            "flexible-server",
            "create",
            "--resource-group",
            self.resource_group,
            "--name",
            self.db_server_name,  # Flag is --name for the engine creation
            "--admin-user",
            self.admin_user,
            "--admin-password",
            self.admin_password,
            "--location",
            self.location,
            "--tier",
            "Burstable",  # Explicitly set to avoid expensive defaults
            "--sku-name",
            "Standard_B1ms",
            "--public-access",
            "0.0.0.0",  # Required for your local machine/GitHub to talk to it
            "--yes",  # CRITICAL: Prevents the script from hanging on a prompt
        ]

    @override
    def get_cmd_create_database_schema(self) -> list:
        """
        Returns Azure Flexible MySQL CLI command as a string for creating
        a new database instance on the server.
        """
        print(
            f"[{self.PROVIDER_NAME}] Generating CLI command to create DB: {self.database_name}"
        )

        # We join the list into a single string so run_cmd_with_retries can execute it
        return [
            "az",
            "mysql",
            "flexible-server",
            "db",
            "create",
            "--resource-group",
            self.resource_group,
            "--server-name",
            self.db_server_name,
            "--database-name",
            self.database_name,
        ]

    @override
    def get_cmd_db_exists(self) -> list:
        """
        Returns the Azure CLI command to check if a specific database exists
         on the MySQL Flexible Server.
        """
        print(
            f"[{self.PROVIDER_NAME}] Checking existence of DB: {self.database_name} on {self.db_server_name}..."
        )

        return [
            "az",
            "mysql",
            "flexible-server",
            "db",
            "show",
            "--resource-group",
            self.resource_group,
            "--server-name",
            self.db_server_name,
            "--database-name",
            self.database_name,
        ]

    @override
    def get_cmd_engine_exists(self) -> list:
        """
        Returns the Azure CLI command to check if the MySQL Flexible Server
        engine/instance exists.
        """
        print(
            f"[{self.PROVIDER_NAME}] Checking existence of Engine: {self.db_server_name}..."
        )

        return [
            "az",
            "mysql",
            "flexible-server",
            "show",  # No 'db' here
            "--resource-group",
            self.resource_group,
            "--name",  # Note: 'show' for the engine uses --name, not --server-name
            self.db_server_name,
        ]
