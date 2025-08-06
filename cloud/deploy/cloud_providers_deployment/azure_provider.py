from dotenv import load_dotenv
import os

from .base_provider import BaseCloudProvider

load_dotenv()

class AzureCloudProvider(BaseCloudProvider):
    def __init__(self, context):
        self.acr_name = os.getenv(f"AZURE_{context}_acr_name")
        self.resource_group = os.getenv(f"AZURE_{context}_resource_group")
        self.environment_name = os.getenv(f"AZURE_{context}_environment_name")
        return

    def get_build_cmd(self, dockerfile, package_path, tag):
        """
        Build and push the Docker image to Azure Container Registry (ACR).
        Assumes the ACR is already created and user is logged in via az.
        """
        acr_name = self.acr_name
        full_tag = f"{acr_name}.azurecr.io/{tag}"

        return [
            # Step 1: Build the image locally
            ["docker", "build", "-f", dockerfile, "-t", full_tag, package_path],
            # Step 2: Login to ACR
            ["az", "acr", "login", "--name", acr_name],
            # Step 3: Push the image to ACR
            ["docker", "push", full_tag],
        ]

    def get_run_cmd(self, image_name, tag, **kwargs):
        """
        Deploys a container to Azure Container Apps (ACA).
        Assumes the container image is already pushed to ACR.
        """
        acr_name = self.acr_name
        full_tag = f"{acr_name}.azurecr.io/{tag}"
        container_app_name = image_name.lower().replace("_", "-") + "-app"
        resource_group = self.resource_group
        environment_name = self.environment_name

        return [
            "az", "containerapp", "create",
            "--name", container_app_name,
            "--resource-group", resource_group,
            "--environment", environment_name,
            "--image", full_tag,
            "--target-port", "80",
            "--ingress", "external",
            "--registry-server", f"{acr_name}.azurecr.io",
            "--min-replicas", "1",
            "--max-replicas", "1"
        ]