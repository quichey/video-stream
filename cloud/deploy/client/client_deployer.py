from common.base import BaseDeployer
from common.mixins.package_manager_mixin import PackageManagerMixin
from common.mixins.docker_mixin import DockerMixin
from common.mixins.cloud_mixin import CloudMixin
from common.mixins.bashrc_mixin import BashrcMixin

class ClientDeployer(BaseDeployer, PackageManagerMixin, DockerMixin, CloudMixin, BashrcMixin):
    CONTEXT = "client"
    PACKAGE_MANAGER = "npm"
    PACKAGE_PATH = f"{BaseDeployer.PATH_PROJECT_ROOT}/{CONTEXT}"
    IMAGE_NAME = f"{CONTEXT}-engine"
    DOCKERFILE = f"{BaseDeployer.PATH_PROJECT_DOCKER}/{CONTEXT}/{CONTEXT}.Dockerfile"
    TAG = f"gcr.io/my-project/{CONTEXT}-engine:1.0.0"

    # AZURE VARIABLES
    ACR_NAME = "a"
    RESOURCE_GROUP = "a"
    ENVIRONMENT_NAME = "a"

    def __init__(self, provider_name, acr_name, resource_group, environment_name):
        super().__init__(provider_name, self.ACR_NAME, self.RESOURCE_GROUP, self.ENVIRONMENT_NAME)