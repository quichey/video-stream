import os
import sys
from dotenv import load_dotenv
from subprocess import run, CalledProcessError
from cloud_providers_deployment.base.base_provider import BaseCloudProvider

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from providers.azure.azure_cli import AzureCLIHelper

load_dotenv()
load_dotenv(dotenv_path="../providers/azure/.env")


class AzureBaseProvider(BaseCloudProvider):
    PROVIDER_NAME = "azure"

    def __init__(self, context, env):
        super().__init__(context, env)
        self._acr_name = os.environ.get("CONTAINER_REGISTRY_NAME", "blah")
        self._acr_user_name = os.environ.get("CONTAINER_REGISTRY_USER_NAME", "blah")
        self._acr_user_password = os.environ.get(
            "CONTAINER_REGISTRY_USER_PASSWORD", "blah"
        )
        self._resource_group = os.environ.get("RESOURCE_GROUP_CENTRAL", "blah")
        self._location = os.environ.get("AZURE_LOCATION", "westus2")

        cli_helper = AzureCLIHelper(
            resource_group=self.resource_group, acr_name=self.acr_name
        )
        cli_helper.login()

    @property
    def acr_name(self) -> str:
        return self._acr_name

    @property
    def acr_user_name(self) -> str:
        return self._acr_user_name

    @property
    def acr_user_password(self) -> str:
        return self._acr_user_password

    @property
    def resource_group(self) -> str:
        return self._resource_group

    @property
    def location(self) -> str:
        return self._location

    def _run_az_cmd(self, cmd: list):
        try:
            run(cmd, check=True)
        except CalledProcessError as e:
            print(f"[AzureDBCloudProvider] Command failed: {' '.join(cmd)}")
            raise e
