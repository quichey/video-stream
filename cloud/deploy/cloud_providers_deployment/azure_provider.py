from dotenv import load_dotenv
import os

from .base_provider import BaseCloudProvider

load_dotenv()
load_dotenv(dotenv_path="../providers/azure/.env")

class AzureProvider(BaseCloudProvider):
    def __init__(self, context):
        self.acr_name = os.environ.get("CONTAINER_REGISTRY_NAME", 'blah')
        self.resource_group = os.environ.get("RESOUCE_GROUP_CENTRAL", 'blah')
        self.environment_name = os.getenv(f"CONTAINER_APP_ENVIRONMENT")
  
        self.image_name = f"{context}-engine"
        self.container_app_name = self.image_name.lower().replace("_", "-") + "-app"
        self.tag = f"{self.acr_name}.azurecr.io/{context}-engine:1.0.0"
        return

    def get_build_cmd(self, dockerfile, package_path):
        """
        Build and push the Docker image to Azure Container Registry (ACR).
        Assumes the ACR is already created and user is logged in via az.
        """

        return [
            # Step 1: Build the image locally
            ["docker", "build", "-f", dockerfile, "-t", self.tag, package_path],
            # Step 2: Login to ACR
            ["az", "acr", "login", "--name", self.acr_name],
            # Step 3: Push the image to ACR
            ["docker", "push", self.tag],
        ]

    def get_run_cmd(self):
        """
        Deploys a container to Azure Container Apps (ACA).
        Assumes the container image is already pushed to ACR.
        """

        return [
            "az", "containerapp", "create",
            "--name", self.container_app_name,
            "--resource-group", self.resource_group,
            "--environment", self.environment_name,
            "--image", self.tag,
            "--target-port", "80",
            "--ingress", "external",
            "--registry-server", f"{self.acr_name}.azurecr.io",
            "--min-replicas", "1",
            "--max-replicas", "1"
        ]