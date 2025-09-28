from cloud_providers_deployment import get_provider_class_db
from common.mixins.cloud_mixin.cloud_mixin import CloudMixin


def pre_build_hook(func):
    """Decorator to run a pre-build step if the subclass/provider defines it."""

    def wrapper(self, *args, **kwargs):
        # Call pre-build step if provider has it
        pre_build = getattr(self.provider, "pre_build_image_cloud", None)
        if callable(pre_build):
            print(f"[CloudMixin] Running pre-build step for {self.context}...")
            pre_build(*args, **kwargs)
        return func(self, *args, **kwargs)

    return wrapper


class CloudDBMixin(CloudMixin):
    GET_PROVIDER_CLASS_FUNC = get_provider_class_db

    def set_up_provider_env(self):
        self.provider.set_up_env()
        return

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
