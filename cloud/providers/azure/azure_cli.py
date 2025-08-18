import subprocess
from dotenv import load_dotenv
import os


load_dotenv(dotenv_path="./azure/.env")

class AzureCLIHelper:
    def __init__(self, resource_group: str, acr_name: str, location: str = "westus"):
        self.resource_group = resource_group
        self.acr_name = acr_name
        self.location = location

    def run_cmd(self, cmd_list):
        """Run a shell command list and print output; raise if fails."""
        print(f"Running: {' '.join(cmd_list)}")
        result = subprocess.run(cmd_list, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr.strip()}")
            raise RuntimeError(f"Command failed: {' '.join(cmd_list)}")
        print(result.stdout.strip())
        return result.stdout.strip()

    def login(self):
        """Login to Azure CLI."""
        return self.run_cmd([
            "az", "login",
            "--service-principal",
            "--username", os.getenv("CLIENT_ID"),
            "--password", os.getenv("CLIENT_SECRET_VALUE"),
            "--tenant", os.getenv("TENANT_ID"),
        ])

    def create_resource_group(self):
        """Create resource group if it doesn't exist."""
        return self.run_cmd([
            "az", "group", "create",
            "--name", self.resource_group,
            "--location", self.location
        ])

    def create_acr(self, sku="Basic"):
        """Create Azure Container Registry."""
        return self.run_cmd([
            "az", "acr", "create",
            "--resource-group", self.resource_group,
            "--name", self.acr_name,
            "--sku", sku,
            "--location", self.location
        ])

    def acr_login(self):
        """Login to Azure Container Registry."""
        return self.run_cmd(["az", "acr", "login", "--name", self.acr_name])

    def push_docker_image(self, image_tag):
        """Push a Docker image to ACR."""
        full_tag = f"{self.acr_name}.azurecr.io/{image_tag}"
        self.run_cmd(["docker", "tag", image_tag, full_tag])
        self.acr_login()
        return self.run_cmd(["docker", "push", full_tag])

    def deploy_container_app(self, app_name, image_tag, environment_name):
        """Deploy an Azure Container App."""
        full_tag = f"{self.acr_name}.azurecr.io/{image_tag}"
        return self.run_cmd([
            "az", "containerapp", "create",
            "--name", app_name,
            "--resource-group", self.resource_group,
            "--environment", environment_name,
            "--image", full_tag,
            "--target-port", "80",
            "--ingress", "external",
            "--registry-server", f"{self.acr_name}.azurecr.io",
            "--min-replicas", "1",
            "--max-replicas", "1"
        ])

    """
    Enables Auto-Stop on an Azure MySQL Flexible Server instance.

    Args:
        server_name (str): Name of the MySQL Flexible Server instance.
        resource_group (str): Azure Resource Group containing the server.
        auto_stop_delay_minutes (int): Idle time in minutes before auto-stop triggers. Default is 60.

    Returns:
        bool: True if command succeeded, False otherwise.
    """
    def enable_mysql_flexible_auto_stop(self, server_name: str, resource_group: str, auto_stop_delay_minutes: int = 60):
        cmd = [
            "az", "mysql", "flexible-server", "update",
            "--name", server_name,
            "--resource-group", resource_group,
            "--auto-stop-enabled", 'true',
            #"--auto-stop-delay", str(auto_stop_delay_minutes)
        ]

        try:
            print(f"Running command to enable Auto-Stop: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"Auto-Stop enabled on server '{server_name}' with delay {auto_stop_delay_minutes} minutes.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to enable Auto-Stop: {e}")
            return False