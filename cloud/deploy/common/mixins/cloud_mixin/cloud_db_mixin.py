from cloud_providers_deployment import get_provider_class_db
from common.mixins.cloud_mixin.cloud_mixin import CloudMixin
from util.subprocess_helper import (
    run_cmd_with_retries,
    run_shell_command,
    check_command_success,
)


class CloudDBMixin(CloudMixin):
    GET_PROVIDER_CLASS_FUNC = get_provider_class_db

    def is_first_deploy(self) -> bool:
        """
        check if database engine is already deployed
        """
        cloud_cmd = self.provider.get_cmd_engine_exists()
        print(f"[CloudDBMixin] Checking if db engine exists {self.context} on Cloud...")
        # TODO: check if get_cmd_engine_exists will work with check_command
        return check_command_success(cloud_cmd)

    def provision_database_engine(self):
        """
        Provision the database itself.
        For example, create SQL server, Postgres instance, or Cosmos DB.
        """
        cloud_cmd = self.provider.get_cmd_provision_database_engine()
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

    def seed_database(self):
        """
        Sequence:
        1. Find the seeded_db.sql file.
        2. Pipe it into the Cloud DB using the provider's command.
        3. Use Alembic to 'stamp' the DB so it knows it is at the initial version.
        """
        # Using the new bool helper
        cloud_cmd = self.provider.get_cmd_db_exists()

        # This is now a clean boolean check
        if not check_command_success(cloud_cmd):
            print(f"[CloudDBMixin] Schema {self.context} not found. Creating...")
            create_cmd = self.provider.get_cmd_create_database_schema()
            run_cmd_with_retries(create_cmd, check=True)
        else:
            print(f"[CloudDBMixin] Schema {self.context} already exists.")

        # 1. Locate the SQL file relative to the execution path (cloud/deploy)
        sql_file_path = "seeded_db.sql"

        # 2. Get the  command from the provider (Azure/AWS/etc)
        full_load_cmd = self.provider.get_load_db_cmd(sql_file_path)

        print(f"[CloudDBMixin] Seeding database using {sql_file_path}...")

        # Execute the load. We use shell=True because of the '<' redirection.
        run_shell_command(full_load_cmd, check=True)

        # 3. Handle the Alembic Stamp
        def run_alembic_stamp():
            # Based on your structure:
            # We are in cloud/deploy.
            # Server is at ../../server relative to this file?
            # Usually better to use an absolute path or project root.
            SERVER_ROOT_PATH = "../../server"

            # The 'stamp' command tells Alembic:
            # "The DB is already at this version, don't try to re-run it."
            # We use the Revision ID from your version file: 6954f76c47c2
            # TODO: use my predefined alembic sub-module under server i think
            target_revision = "6954f76c47c2"

            cmd = f"cd {SERVER_ROOT_PATH} && poetry run alembic stamp {target_revision}"

            print(f"[CloudDBMixin] Stamping database at revision {target_revision}...")
            run_shell_command(cmd, check=True, shell=True)

        run_alembic_stamp()
        print("[CloudDBMixin] Database seeding and stamping complete.")
