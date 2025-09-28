from abc import ABC, abstractmethod
from dotenv import load_dotenv
import shutil

from common.mixins.cloud_mixin.cloud_db_mixin import CloudDBMixin
from common.base import BaseDeployer


load_dotenv()


def pre_set_up_cloud_env_hook(func):
    """Decorator to run a pre-set-up-cloud-env step if the subclass/provider defines it."""

    def wrapper(self, *args, **kwargs):
        # Call pre-build step if provider has it
        pre_build = getattr(self, "pre_set_up_cloud_env", None)
        if callable(pre_build):
            print(
                f"[BaseDeployer] Running pre-set-up-cloud-env step for {self.CONTEXT}..."
            )
            pre_build(*args, **kwargs)
        return func(self, *args, **kwargs)

    return wrapper


# TODO: db deploy
class BaseDBDeployer(BaseDeployer, ABC):
    CLOUD_MIXIN_CLASS = CloudDBMixin

    @abstractmethod
    def deploy(self):
        print(f"=== Deploying {self.CONTEXT} Database ===")
        self.set_up_cloud_env()
        self.provision_database()
        self.run_migrations()
        self.clean_up()

    def verify_os_env(self):
        """Shared OS environment verification based on package_manager."""
        if self.PACKAGE_MANAGER == "npm":
            for tool in ["node", "npm"]:
                if shutil.which(tool) is None:
                    raise EnvironmentError(
                        f"{tool} not found. Run deploy/os/linux/env_setup.sh first."
                    )
        elif self.PACKAGE_MANAGER == "poetry":
            if shutil.which("poetry") is None:
                raise EnvironmentError(
                    "poetry not found. Run deploy/os/linux/env_setup.sh first."
                )
        else:
            raise ValueError(f"Unknown package manager: {self.PACKAGE_MANAGER}")

    @pre_set_up_cloud_env_hook
    def set_up_cloud_env(self):
        if self.is_cloud():
            print(f"[BaseDeployer] Setting Up Cloud Provider env for {self.CONTEXT}")
            self.cloud_mixin_instance.set_up_provider_env()
        else:
            print(
                f"[BaseDeployer] Local Deploy: Skipping Cloud env setup for {self.CONTEXT}"
            )

        return

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

        Use server/Seed module here i think
        """
        pass

    @abstractmethod
    def clean_up(self):
        """
        Clean up temporary resources or connections after deploy.
        """
        pass
