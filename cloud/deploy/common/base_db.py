from abc import ABC, abstractmethod
from dotenv import load_dotenv

from common.mixins.cloud_mixin.cloud_db_mixin import CloudDBMixin
from common.base import BaseDeployer


load_dotenv()


# TODO: db deploy
class BaseDBDeployer(BaseDeployer, ABC):
    CLOUD_MIXIN_CLASS = CloudDBMixin

    def deploy(self):
        print(f"=== Deploying {self.CONTEXT} Database ===")
        self.set_up_cloud_env()
        self.provision_database()
        self.run_migrations()
        self.clean_up()

    def provision_database(self):
        """
        Provision the database itself.
        For example, create SQL server, Postgres instance, or Cosmos DB.
        """
        pass

    def run_migrations(self):
        """
        Run any schema migrations or initialization scripts.

        Use server/Seed module here i think
        """
        pass

    @abstractmethod
    def clean_up(self):
        """
        Clean up temporary resources or connections after deploy.
        """
        pass
