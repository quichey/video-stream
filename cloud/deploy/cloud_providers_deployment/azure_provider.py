from dotenv import load_dotenv
from typing_extensions import override
import os
import sys

from util.subprocess_helper import run_cmd_with_retries
from common.mixins.docker_mixin import DockerMixin

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from providers.azure.azure_cli import AzureCLIHelper
from .base_provider import BaseCloudProvider

load_dotenv()
load_dotenv(dotenv_path="../providers/azure/.env")


class AzureProvider(BaseCloudProvider, DockerMixin):
    PROVIDER_NAME = "azure"

    def __init__(self, context, env):
        super().__init__(context, env)
        self.acr_name = os.environ.get("CONTAINER_REGISTRY_NAME", "blah")
        self.acr_login_server = os.environ.get(
            "CONTAINER_REGISTRY_LOGIN_SERVER", "blah"
        )
        self.acr_user_name = os.environ.get("CONTAINER_REGISTRY_USER_NAME", "blah")
        self.acr_user_password = os.environ.get(
            "CONTAINER_REGISTRY_USER_PASSWORD", "blah"
        )
        self.resource_group = os.environ.get("RESOURCE_GROUP_CENTRAL", "blah")
        self.environment_name = os.getenv("CONTAINER_APP_ENVIRONMENT")

        self.container_app_name = (
            self.image.repository.lower().replace("_", "-") + "-app"
        )
        self.image.registry = f"{self.acr_login_server}.azurecr.io"

        cli_helper = AzureCLIHelper(
            resource_group=self.resource_group, acr_name=self.acr_name
        )
        cli_helper.login()
        return

    @override
    def get_restart_cmd(self):
        return [
            "az",
            "container",
            "restart",
            "--name",
            self.container_app_name,
            "--resource-group",
            self.resource_group,
        ]

    @override
    def get_stop_cmd(self):
        return [
            "az",
            "container",
            "stop",
            "--name",
            self.container_app_name,
            "--resource-group",
            self.resource_group,
        ]

    @override
    def get_start_cmd(self):
        return [
            "az",
            "container",
            "start",
            "--name",
            self.container_app_name,
            "--resource-group",
            self.resource_group,
        ]

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
        if self.ENV == "prod":
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
        else:
            cmd = [
                "az",
                "container",
                "show",
                "--name",
                self.container_app_name,
                "--resource-group",
                self.resource_group,
                "--query",
                "ipAddress.fqdn",
                "-o",
                "tsv",
            ]
        return run_cmd_with_retries(cmd)

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
        if self.ENV == "prod":
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
        else:
            # dev/test → ACI
            dns_label = f"{self.container_app_name}-{self.ENV}"  # optional
            return [
                "az",
                "container",
                "create",
                "--name",
                self.container_app_name,
                "--resource-group",
                self.resource_group,
                "--image",
                self.image.full_name,
                "--cpu",
                "0.5",
                "--memory",
                "1",
                "--registry-login-server",
                f"{self.acr_login_server}.azurecr.io",
                "--registry-username",
                self.acr_user_name,
                "--registry-password",
                self.acr_user_password,
                "--dns-name-label",
                dns_label,
                "--ports",
                "8080",
                "--os-type",
                "Linux",
            ]
