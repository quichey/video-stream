from abc import ABC, abstractmethod

from cloud_providers_deployment.base.base_provider import BaseCloudProvider


class BaseDBCloudProvider(BaseCloudProvider, ABC):
    """
    Abstract base class for cloud database providers.
    Handles DB provisioning, migrations, and deletion.
    """

    def __init__(self, context, env):
        super().__init__(context, env)
        self._engine_name = (
            f"{context}-engine" if env == "prod" else f"{context}-engine-{env}"
        )
        self._db_name = self._engine_name

    @property
    def engine_name(self) -> str:
        return self._engine_name

    @property
    def db_name(self) -> str:
        return self._db_name

    @abstractmethod
    def get_cmd_provision_database_engine(self) -> list:
        """Provision a new database engine instance."""
        pass

    @abstractmethod
    def get_cmd_create_database_schema(self) -> list:
        """Create a new database schema instance."""
        pass

    @abstractmethod
    def get_cmd_run_migrations(self) -> str:
        """Run migrations or schema setup on the database."""
        pass

    @abstractmethod
    def get_cmd_delete_database(self) -> str:
        """Delete a database instance."""
        pass

    @abstractmethod
    def get_connection_string(self) -> str:
        """Return connection string / URI for the database."""
        pass

    @abstractmethod
    def get_load_db_cmd(self, sql_file) -> str:
        """Return command to load data into db"""
        pass

    @abstractmethod
    def get_cmd_db_exists(self) -> list:
        """Return command to check if db exists"""
        pass

    @abstractmethod
    def get_cmd_engine_exists(self) -> list:
        """Return command to check if db engine exists"""
        pass
