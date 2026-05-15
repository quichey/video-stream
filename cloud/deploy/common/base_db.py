from abc import ABC, abstractmethod
from dotenv import load_dotenv
from typing_extensions import override
import os
import sys

from common.mixins.cloud_mixin.cloud_db_mixin import CloudDBMixin
from common.base import BaseDeployer

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../server"))
)
from db.Seed import Seed


load_dotenv()


# TODO: db deploy
class BaseDBDeployer(BaseDeployer, ABC):
    CLOUD_MIXIN_CLASS = CloudDBMixin
    CONTEXT = "db"  # override in subclasses if multiple DBs
    ENGINE = None
    SEEDER = None

    def __init__(self, provider_name, env):
        super().__init__(provider_name, env)
        self.SEEDER = Seed()

    @override
    def is_first_deploy(self) -> bool:
        pass

    @override
    def do_first_deploy(self):
        print(f"=== Deploying {self.CONTEXT} Database ===")
        # TODO: handle initial deployment vs subsequent deployments
        self.set_up_cloud_env()
        self.provision_database()
        self.run_migrations()
        self.clean_up()

    @override
    def do_update(self):
        print(f"=== Deploying {self.CONTEXT} Database ===")
        # TODO: handle initial deployment vs subsequent deployments
        self.set_up_cloud_env()
        self.provision_database()
        self.run_migrations()
        self.clean_up()

    def provision_database(self):
        """
        Provision the database itself.
        For example, create SQL server, Postgres instance, or Cosmos DB.
        """
        if self.is_cloud():
            print(f"[BaseDBDeployer] Provisioning for Cloud {self.CONTEXT}")
            self.cloud_mixin_instance.provision_database()
        else:
            print(f"[BaseDBDeployer] Provisioning for Local {self.CONTEXT}")
            self.provision_database_local()
        return

    @abstractmethod
    def provision_database_local(self):
        pass

    def run_migrations(self):
        """
        Run any schema migrations or initialization scripts.

        Use server/Seed module here i think
        """
        if self.is_cloud():
            print(f"[BaseDBDeployer] Provisioning for Cloud {self.CONTEXT}")
            self.cloud_mixin_instance.run_migrations()
        else:
            print(f"[BaseDBDeployer] Provisioning for Local {self.CONTEXT}")
            self.run_migrations_local()
        return

    @abstractmethod
    def run_migrations_local(self):
        pass

    @abstractmethod
    def clean_up(self):
        """
        Clean up temporary resources or connections after deploy.
        """
