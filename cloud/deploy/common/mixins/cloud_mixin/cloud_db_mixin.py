from cloud_providers_deployment import get_provider_class_db
from common.mixins.cloud_mixin.cloud_mixin import CloudMixin


class CloudDBMixin(CloudMixin):
    GET_PROVIDER_CLASS_FUNC = get_provider_class_db

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

    def clean_up(self):
        """
        Clean up temporary resources or connections after deploy.
        """
        pass
