from typing_extensions import override
from subprocess import run, CalledProcessError
from cloud_providers_deployment.base.base_db_provider import BaseDBCloudProvider
from cloud_providers_deployment.azure.azure_base import AzureBaseProvider
from abc import abstractmethod  # Import abc for abstract methods


class AzureDBProvider(AzureBaseProvider, BaseDBCloudProvider):
    # This class acts as the abstract base for all Azure database types (MySQL, Postgres, etc.)
    PROVIDER_NAME = "azure-db-base"

    def __init__(self, context, env):
        super().__init__(context, env)
        # NOTE: Subclasses must define their specific connection and server names.

    def _run_az_cmd(self, cmd: list, action_name: str):
        """Common method to execute the Azure CLI command."""
        try:
            print(f"[{self.PROVIDER_NAME}] Executing {action_name} command...")
            run(cmd, check=True, capture_output=True, text=True)
            print(f"[{self.PROVIDER_NAME}] {action_name} successful.")
        except CalledProcessError as e:
            print(
                f"[{self.PROVIDER_NAME}] {action_name} failed. Command: {' '.join(cmd)}"
            )
            print(f"Stdout:\n{e.stdout}")
            print(f"Stderr:\n{e.stderr}")
            raise e
        except FileNotFoundError:
            print(
                "[ERROR] Azure CLI (az) command not found. Ensure it is installed and in your PATH."
            )
            raise

    # --- Abstract Inner Helper Functions (Must be defined by subclasses) ---

    @abstractmethod
    def _get_server_creation_command(self) -> list:
        """Returns the specific az command list for creating the DB server."""
        pass

    @abstractmethod
    def _get_db_creation_command(self) -> list:
        """Returns the specific az command list for creating the database on the server."""
        pass

    @abstractmethod
    def _get_server_deletion_command(self) -> list:
        """Returns the specific az command list for deleting the DB server."""
        pass

    @abstractmethod
    def get_connection_details(self) -> dict:
        """Returns connection specifics (user, pw, hostname, dbname) for the engine."""
        pass

    # --- Overridden Public API Functions (Call the inner abstract helpers) ---

    @override
    def get_cmd_create_database(self) -> str:
        """Implements the full database provisioning workflow."""
        print(f"[{self.PROVIDER_NAME}] Starting full DB provisioning process...")

        # Step 1: Create the Server
        cmd_server = self._get_server_creation_command()
        self._run_az_cmd(cmd_server, "Server Creation")

        # Step 2: Create the Database on the Server
        cmd_db = self._get_db_creation_command()
        self._run_az_cmd(cmd_db, "Database Creation")

        return "Database server and database creation commands executed."

    @override
    def get_cmd_delete_database(self) -> str:
        """Implements the full database deletion workflow."""
        cmd_delete = self._get_server_deletion_command()
        self._run_az_cmd(cmd_delete, "Server Deletion")
        return "Database server deletion command executed."

    @override
    def get_cmd_run_migrations(self) -> str:
        """Hook for running migrations, delegated to the Deployer class."""
        return "Migration run delegated to Deployer class."
