from dotenv import load_dotenv
from typing_extensions import override
import os
import sys

from common.mixins.docker_mixin import DockerMixin

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from providers.azure.azure_cli import AzureCLIHelper
from .base_provider import BaseCloudProvider

load_dotenv()
load_dotenv(dotenv_path="../providers/azure/.env")

class AzureProvider(BaseCloudProvider, DockerMixin):
    def __init__(self, context):
        super().__init__(context=context)
        self.acr_name = os.environ.get("CONTAINER_REGISTRY_NAME", 'blah')
        self.acr_login_server = os.environ.get("CONTAINER_REGISTRY_LOGIN_SERVER", 'blah')
        self.acr_user_name = os.environ.get("CONTAINER_REGISTRY_USER_NAME", 'blah')
        self.acr_user_password = os.environ.get("CONTAINER_REGISTRY_USER_PASSWORD", 'blah')
        self.resource_group = os.environ.get("RESOURCE_GROUP_CENTRAL", 'blah')
        self.environment_name = os.getenv(f"CONTAINER_APP_ENVIRONMENT")
  
        self.container_app_name = self.image.repository.lower().replace("_", "-") + "-app"
        self.image.registry = f"{self.acr_login_server}.azurecr.io"

        cli_helper = AzureCLIHelper(resource_group=self.resource_group, acr_name=self.acr_name)
        cli_helper.login()
        return

    @override
    def get_latest_image_cmd(self):
        return [
            "az", "acr", "repository", "show-tags",
            "--name", self.image.full_name,
            "--repository", self.image.repository,
            "--orderby", "time_desc",
            "--output", "tsv"
        ]
    
    def pre_build_image_cloud(self, dockerfile, package_path):
        print(f"[AzureProvider] Pre-building Docker image locally...")
        self.build_docker_image_local(image_name=self.image.full_name, dockerfile=dockerfile, package_path=package_path)

    @override
    def get_build_cmd(self, dockerfile, package_path):
        """
        Build and push the Docker image to Azure Container Registry (ACR).
        Assumes the ACR is already created and user is logged in via az.
        """

        return [
            # Step 1: Build the image locally
            #["docker", "build", "-f", dockerfile, "-t", self.tag, package_path],
            # Step 2: Login to ACR
            ["az", "acr", "login", "--name", self.acr_name],
            # Step 3: Push the image to ACR
            ["docker", "push", self.image.full_name],
        ]

    @override
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
            "--image", self.image.full_name,
            "--target-port", "8080",
            "--ingress", "external",
            "--registry-server", f"{self.acr_login_server}.azurecr.io",
            "--registry-username", self.acr_user_name,
            "--registry-password", self.acr_user_password,
            "--min-replicas", "1",
            "--max-replicas", "1"
        ]