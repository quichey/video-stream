# db_deployer.py
from abc import ABC, abstractmethod
from dotenv import load_dotenv

from common.mixins.cloud_mixin import CloudMixin

load_dotenv()


class DBDeployer(ABC):
    """
    Handles deployment of databases in the cloud.
    Designed to work alongside BaseDeployer but for DB provisioning/migrations.
    """

    CONTEXT = "db"  # override in subclasses if multiple DBs

    def __init__(self, provider_name, env):
        self.ENV = env
        print(f"[DBDeployer] Initializing CloudMixin for {self.CONTEXT}...")
        self.cloud_mixin_instance = CloudMixin(
            provider_name=provider_name, context=self.CONTEXT, env=env
        )

    def deploy(self):
        print(f"=== Deploying {self.CONTEXT} Database ===")
        self.set_up_cloud_env()
        self.provision_database()
        self.run_migrations()
        self.clean_up()

    def set_up_cloud_env(self):
        print(f"[DBDeployer] Setting Up Cloud Provider env for {self.CONTEXT}")
        self.cloud_mixin_instance.set_up_provider_env()

    @abstractmethod
    def provision_database(self):
        """
        Provision the database itself.
        For example, create SQL server, Postgres instance, or Cosmos DB.
        """
        pass

    @abstractmethod
    def run_migrations(self):
        """
        Run any schema migrations or initialization scripts.
        """
        pass

    @abstractmethod
    def clean_up(self):
        """
        Clean up temporary resources or connections after deploy.
        """
        pass
