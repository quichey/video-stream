from abc import ABC, abstractmethod
from dotenv import load_dotenv
from typing_extensions import override

from common.mixins.cloud_mixin.cloud_db_mixin import CloudDBMixin
from common.base import BaseDeployer
from util.subprocess_helper import (
    run_shell_command,
)  # Now using the utility


load_dotenv()


# TODO: db deploy
class BaseDBDeployer(BaseDeployer, ABC):
    CLOUD_MIXIN_CLASS = CloudDBMixin
    CONTEXT = "db"  # override in subclasses if multiple DBs
    ENGINE = None

    def __init__(self, provider_name, env):
        super().__init__(provider_name, env, dialect=self.ENGINE)

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

    def run_migrations_local(self):
        print(f"--- Running Local Database Migrations for {self.ENGINE} ---")
        # CRITICAL FIX: The command must change directory (cd) to the server's root
        # to execute within the server's Poetry environment and correct path context.
        # Assuming the server root is two directories up and named 'server'.
        SERVER_ROOT_PATH = "../../server"

        # Command uses 'cd' and shell chaining ('&&') to switch directory before running Poetry.
        cmd = (
            f"cd {SERVER_ROOT_PATH} && "
            f"poetry run python3 -m db.load_db seed --small --dialect {self.ENGINE}"
        )

        print(f"Executing local seeding command (Context: {SERVER_ROOT_PATH})...")

        # Execute the command using the utility function, ensuring failure if the command fails
        run_shell_command(cmd, check=True, shell=True)
        print(f"✅ Local database seeded successfully for {self.ENGINE}.")

    @abstractmethod
    def clean_up(self):
        """
        Clean up temporary resources or connections after deploy.
        """
