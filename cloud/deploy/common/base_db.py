from abc import ABC, abstractmethod
from dotenv import load_dotenv
from typing_extensions import override

from common.mixins.cloud_mixin.cloud_db_mixin import CloudDBMixin
from common.base import BaseDeployer
from util.subprocess_helper import (
    run_shell_command,
)  # Now using the utility

from util.file_handling import update_file

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
        self.seed_database()
        self.clean_up()

    @override
    def do_update(self):
        print(f"=== Updating {self.CONTEXT} Database ===")
        # TODO: handle initial deployment vs subsequent deployments
        self.set_up_cloud_env()
        # TODO: i have been manually reseeding database sometimes instead of
        # migration tools
        # should i do the same for here?
        # probably not
        # make new branch for migration tools?
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

    def seed_database(self):
        """
        Run any schema migrations or initialization scripts.

        Use server/Seed module here i think
        """
        if self.is_cloud():
            print(f"[BaseDBDeployer] Provisioning for Cloud {self.CONTEXT}")
            self.cloud_mixin_instance.seed_database()
        else:
            print(f"[BaseDBDeployer] Provisioning for Local {self.CONTEXT}")
            self.seed_database_local()
        return

    def run_migrations(self):
        """
        Run any schema migrations or initialization scripts.

        Use server/Seed module here i think
        """
        # TODO: update db/migrations/.env file
        # pointing to correct machine depending on self.is_cloud
        # cd to server/ folder first?
        # poetry run alembic ... should be the same for both cases
        dot_env_file_path = "../../server/db/migrations/.env"
        migrations_deployment = "cloud" if self.is_cloud() else "local"
        update_file(
            dot_env_file_path,
            "MIGRATIONS_DEPLOYMENT=",
            f"MIGRATIONS_DEPLOYMENT={migrations_deployment}\n",
        )

        # NOTE: my server/db/ specs code is not great
        # it is hard-coded kinda, would prefer if i had it more config-like using
        # .env files
        # thought of this because as of now, the cloud_mixin_instance.run_migrations
        # is somewhat irrelevant, as migrations/ module has no real way to discern
        # differnt cloud providers without code changes to the db_specs
        if self.is_cloud():
            print(f"[BaseDBDeployer] Provisioning for Cloud {self.CONTEXT}")
            self.cloud_mixin_instance.run_migrations()
        else:
            print(f"[BaseDBDeployer] Provisioning for Local {self.CONTEXT}")
            self.run_migrations_local()
        return

    def run_migrations_local(self):
        # TODO: integrate the migrations code from last branch
        pass

    def seed_database_local(self):
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
