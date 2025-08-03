from deploy.common.base import BaseDeployer
from deploy.common.mixins.package_manager_mixin import PackageManagerMixin
from deploy.common.mixins.docker_mixin import DockerMixin
from deploy.common.mixins.cloud_mixin import CloudMixin
from deploy.common.mixins.bashrc_mixin import BashrcMixin

class ClientDeployer(BaseDeployer, PackageManagerMixin, DockerMixin, CloudMixin, BashrcMixin):
    PACKAGE_MANAGER = "npm"
    PACKAGE_PATH = "client"
    IMAGE_NAME = "client-engine"
    DOCKERFILE = "cloud/Docker/client/client.Dockerfile"
    CONTEXT = "client"
    TAG = "gcr.io/my-project/client-engine:1.0.0"