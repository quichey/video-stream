from typing_extensions import override
from dotenv import load_dotenv

from common.base_db import BaseDBDeployer

load_dotenv()


class MysqlDBDeployer(BaseDBDeployer):
    """
    Handles deployment of databases in the cloud.
    Designed to work alongside BaseDeployer but for DB provisioning/migrations.
    """

    CONTEXT = "db"  # override in subclasses if multiple DBs

    def set_up_cloud_env(self):
        print(f"[DBDeployer] Setting Up Cloud Provider env for {self.CONTEXT}")
        self.cloud_mixin_instance.set_up_provider_env()

    @override
    def provision_database(self):
        """
        Provision the database itself.
        For example, create SQL server, Postgres instance, or Cosmos DB.
        """
        pass

    @override
    def run_migrations(self):
        """
        Run any schema migrations or initialization scripts.

        Use server/Seed module here i think
        """
        pass

    @override
    def clean_up(self):
        """
        Clean up temporary resources or connections after deploy.
        """
        pass
