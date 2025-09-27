from abc import ABC, abstractmethod

from cloud_providers_deployment.base.base_provider import BaseCloudProvider


class BaseDBCloudProvider(BaseCloudProvider, ABC):
    """
    Abstract base class for cloud database providers.
    Handles DB provisioning, migrations, and deletion.
    """

    def __init__(self, context, env):
        self.context = context
        self.env = env

    @abstractmethod
    def create_database(self, db_name: str):
        """Create a new database instance."""
        pass

    @abstractmethod
    def run_migrations(self, db_name: str):
        """Run migrations or schema setup on the database."""
        pass

    @abstractmethod
    def delete_database(self, db_name: str):
        """Delete a database instance."""
        pass

    @abstractmethod
    def get_connection_string(self, db_name: str) -> str:
        """Return connection string / URI for the database."""
        pass
