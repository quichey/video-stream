from cloud_providers_deployment import get_provider_class_db
from common.mixins.cloud_mixin.cloud_mixin import CloudMixin
from util.subprocess_helper import run_cmd_with_retries


class CloudDBMixin(CloudMixin):
    GET_PROVIDER_CLASS_FUNC = get_provider_class_db

    def provision_database(self):
        """
        Provision the database itself.
        For example, create SQL server, Postgres instance, or Cosmos DB.
        """
        cloud_cmd = self.provider.get_cmd_create_database()
        print(f"[CloudDBMixin] Provisioning {self.context} to Cloud...")
        run_cmd_with_retries(
            cloud_cmd,
            check=True,
        )

    def run_migrations(self):
        """
        Run any schema migrations or initialization scripts.

        Use server/Seed module here i think
        """
        cloud_cmd = self.provider.get_cmd_run_migrations()
        print(f"[CloudDBMixin] Running migrations {self.context} on Cloud...")
        run_cmd_with_retries(
            cloud_cmd,
            check=True,
        )

    def clean_up(self):
        """
        Clean up temporary resources or connections after deploy.
        """
        cloud_cmd = self.provider.get_run_cmd()
        print(f"[CloudDBMixin] Provisioning {self.context} to Cloud...")
        run_cmd_with_retries(
            cloud_cmd,
            check=True,
        )

    def seed_database(eelf):
        # TODO: take the archived copy of initial db state?
        # and load it into the cloud database?
        # and then run alembic stamp?

        # testing git config
        pass
