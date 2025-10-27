from dotenv import load_dotenv
from typing_extensions import override
import os

from util.subprocess_helper import run_cmd_with_retries
from common.mixins.docker_mixin import DockerMixin
from cloud_providers_deployment.base.base_container_provider import (
    BaseCloudContainerProvider,
)
from cloud_providers_deployment.azure.azure_base import AzureBaseProvider


load_dotenv()
load_dotenv(dotenv_path="../providers/azure/.env")


class AzureContainerProvider(
    AzureBaseProvider, BaseCloudContainerProvider, DockerMixin
):
    def __init__(self, context, env):
        super().__init__(context, env)
        self.acr_login_server = os.environ.get(
            "CONTAINER_REGISTRY_LOGIN_SERVER", "blah"
        )
        self.environment_name = os.getenv("CONTAINER_APP_ENVIRONMENT")

        self.container_app_name = (
            self.image.repository.lower().replace("_", "-") + "-app"
        )
        self.image.registry = f"{self.acr_login_server}.azurecr.io"
        return

    @override
    def get_latest_image_cmd(self):
        return [
            "az",
            "acr",
            "repository",
            "show-tags",
            "--name",
            self.acr_name,
            "--repository",
            self.image.repository,
            "--orderby",
            "time_desc",
            "--output",
            "tsv",
        ]

    @override
    def get_container_url(self):
        cmd = [
            "az",
            "containerapp",
            "show",
            "--name",
            self.container_app_name,
            "--resource-group",
            self.resource_group,
            "--query",
            "properties.configuration.ingress.fqdn",
            "-o",
            "tsv",
        ]
        app_url = run_cmd_with_retries(cmd)
        return app_url

    def pre_build_image_cloud(self, dockerfile, package_path):
        print("[AzureProvider] Pre-building Docker image locally...")
        self.build_docker_image_local(
            image_name=self.image.full_name,
            dockerfile=dockerfile,
            package_path=package_path,
        )

    @override
    def get_build_cmd(self, dockerfile, package_path):
        """
        Build and push the Docker image to Azure Container Registry (ACR).
        Assumes the ACR is already created and user is logged in via az.
        """
        print(f"\n\n self.image.full_name: {self.image.full_name}")
        return [
            # Step 1: Build the image locally
            # ["docker", "build", "-f", dockerfile, "-t", self.tag, package_path],
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
            "az",
            "containerapp",
            "create",
            "--name",
            self.container_app_name,
            "--resource-group",
            self.resource_group,
            "--environment",
            self.environment_name,
            "--image",
            self.image.full_name,
            "--target-port",
            "8080",
            "--ingress",
            "external",
            "--registry-server",
            f"{self.acr_login_server}.azurecr.io",
            "--registry-username",
            self.acr_user_name,
            "--registry-password",
            self.acr_user_password,
            "--min-replicas",
            "1",
            "--max-replicas",
            "1",
        ]
