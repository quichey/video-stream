from common.base import BaseDeployer
from common.mixins.package_manager_mixin import PackageManagerMixin
from common.mixins.docker_mixin import DockerMixin
from common.mixins.cloud_mixin import CloudMixin
from common.mixins.bashrc_mixin import BashrcMixin

class ServerDeployer(BaseDeployer, PackageManagerMixin, DockerMixin, CloudMixin, BashrcMixin):
    CONTEXT = "server"
    PACKAGE_MANAGER = "poetry"
    PACKAGE_PATH = f"{BaseDeployer.PATH_PROJECT_ROOT}/{CONTEXT}"
    IMAGE_NAME = f"{CONTEXT}-engine"
    DOCKERFILE = f"{BaseDeployer.PATH_PROJECT_DOCKER}/{CONTEXT}/{CONTEXT}.Dockerfile"
    TAG = f"gcr.io/my-project/{CONTEXT}-engine:1.0.0"
