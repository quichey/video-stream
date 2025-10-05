from typing_extensions import override
from dotenv import load_dotenv
import subprocess

from common.base_db import BaseDBDeployer
from util.subprocess_helper import (
    run_shell_command,
    get_os_type,
)  # Now using the utility

load_dotenv()


class MysqlDBDeployer(BaseDBDeployer):
    """
    Handles deployment of databases in the cloud and local environments for MySQL.
    """

    ENGINE = "mysql"

    def set_up_cloud_env(self):
        print(f"[DBDeployer] Setting Up Cloud Provider env for {self.CONTEXT}")
        self.cloud_mixin_instance.set_up_provider_env()

    @override
    def provision_database_local(self):
        """
        Provision the local MySQL database instance. This checks if the client/server
        is installed and attempts to ensure the server is running.

        We avoid interactive installation arguments as they are non-standard
        and often fail in automated scripts.
        """
        print("[MySQL Deployer] Checking for local MySQL installation...")

        # 1. Check if the 'mysql' client command is available in PATH
        try:
            # Running 'mysql --version' verifies both binary presence and execution
            run_shell_command("mysql --version", check=True)
            print("✅ MySQL client found in PATH.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            os_type = get_os_type()
            print("❌ MySQL client not found or failed to execute.")

            # Provide OS-specific installation hints (user must install manually)
            print(f"--- LOCAL INSTALLATION REQUIRED (OS: {os_type}) ---")
            if os_type == "Darwin":  # macOS
                print(
                    "Hint: Install using Homebrew: 'brew install mysql' and follow setup instructions."
                )
            elif os_type == "Linux":  # Linux (Debian/Ubuntu)
                print(
                    "Hint: Install using apt: 'sudo apt update && sudo apt install mysql-server'"
                )
            elif os_type == "Windows":
                print("Hint: Install using the official MySQL Installer or Chocolatey.")

            raise SystemExit(
                "Local MySQL installation is required. Please install it and re-run."
            )

        # 2. Check and start the MySQL service (highly OS/setup dependent)
        print("[MySQL Deployer] Attempting to start/verify MySQL server status...")

        os_type = get_os_type()
        start_command = None

        if os_type == "Darwin":  # macOS (Homebrew service)
            start_command = "brew services start mysql"
        elif os_type == "Linux":  # Linux (systemd)
            start_command = "sudo systemctl start mysql"

        if start_command:
            print(f"Attempting service startup via: '{start_command}'")
            # We use 'check=False' because starting an already-running service often
            # returns a non-zero exit code which shouldn't fail the whole deploy.
            run_shell_command(start_command, check=False, shell=True)
        else:
            print("Note: Automatic service startup command not available for this OS.")

        print("Local MySQL provisioning complete. The server should be running.")
        print(
            "Final step: Ensure your environment variables (DB_USER, DB_PASSWORD, etc.) are set."
        )

    @override
    def clean_up(self):
        """
        Clean up temporary resources or connections after deploy.
        """
        pass
