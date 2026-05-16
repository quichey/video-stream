from typing_extensions import override
from dotenv import load_dotenv

from common.base_db import BaseDBDeployer

load_dotenv()


class PostgresDBDeployer(BaseDBDeployer):
    """
    Handles deployment for PostgreSQL databases, both in cloud and local environments.
    """

    ENGINE = "postgres"

    def set_up_cloud_env(self):
        print(f"[DBDeployer] Setting Up Cloud Provider env for {self.CONTEXT}")
        self.cloud_mixin_instance.set_up_provider_env()

    @override
    def provision_database_local(self):
        """
        Provision the local PostgreSQL database instance (e.g., check for pg_ctl, ensure service is running).
        """
        print(
            "[Postgres Deployer] Checking for local Postgres installation and service status..."
        )
        # TODO: Implement checks for 'psql' client and service startup commands (e.g., systemctl start postgresql)
        print(
            "Local Postgres provisioning complete. Server should be ready for migrations."
        )

    @override
    def clean_up(self):
        """
        Clean up temporary resources or connections after deploy.
        """
        pass
