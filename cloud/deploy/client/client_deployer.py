from common.base import BaseDeployer
from common.mixins.package_manager_mixin import PackageManagerMixin
from common.mixins.docker_mixin import DockerMixin
from common.mixins.cloud_mixin import CloudMixin
from common.mixins.bashrc_mixin import BashrcMixin

class ClientDeployer(BaseDeployer, PackageManagerMixin, DockerMixin, CloudMixin, BashrcMixin):
    PACKAGE_MANAGER = "npm"
    PACKAGE_PATH = f"{BaseDeployer.PATH_PROJECT_ROOT}/client"
    IMAGE_NAME = "client-engine"
    DOCKERFILE = f"{BaseDeployer.PATH_PROJECT_DOCKER}/client/client.Dockerfile"
    CONTEXT = "client"
    TAG = "gcr.io/my-project/client-engine:1.0.0"