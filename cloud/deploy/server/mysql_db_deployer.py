from typing_extensions import override
from dotenv import load_dotenv

from common.base_db import BaseDBDeployer

load_dotenv()


class MysqlDBDeployer(BaseDBDeployer):
    """
    Handles deployment of databases in the cloud.
    Designed to work alongside BaseDeployer but for DB provisioning/migrations.
    """

    ENGINE = "mysql"

    def set_up_cloud_env(self):
        print(f"[DBDeployer] Setting Up Cloud Provider env for {self.CONTEXT}")
        self.cloud_mixin_instance.set_up_provider_env()

    @override
    def provision_database_local(self):
        """
        Provision the database itself.
        For example, create SQL server, Postgres instance, or Cosmos DB.
        """
        #TODO: handle mysql installation or something

    @override
    def run_migrations_local(self):
        """
        Run any schema migrations or initialization scripts.

        Use server/Seed module here i think
        """
        #TODO: do things
        # want the Seed thing to specifically be mysql
        # think need to update Seed module some more
        testing_state = pass
        self.SEEDER.initiate_test_environment(testing_state)

    @override
    def clean_up(self):
        """
        Clean up temporary resources or connections after deploy.
        """
        pass
