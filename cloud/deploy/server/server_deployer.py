from common.base import BaseDeployer
from common.mixins.package_manager_mixin import PackageManagerMixin
from common.mixins.docker_mixin import DockerMixin
from common.mixins.cloud_mixin import CloudMixin
from common.mixins.bashrc_mixin import BashrcMixin

class ServerDeployer(BaseDeployer, PackageManagerMixin, DockerMixin, CloudMixin, BashrcMixin):
    PACKAGE_MANAGER = "poetry"
    PACKAGE_PATH = f"{BaseDeployer.PATH_PROJECT_ROOT}/server"
    IMAGE_NAME = "server-engine"
    DOCKERFILE = f"{BaseDeployer.PATH_PROJECT_DOCKER}/server/server.Dockerfile"
    CONTEXT = "server"
    TAG = "gcr.io/my-project/server-engine:1.0.0"
