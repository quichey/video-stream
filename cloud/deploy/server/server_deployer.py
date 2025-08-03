from deploy.common.base import BaseDeployer
from deploy.common.mixins.docker_mixin import DockerMixin
from deploy.common.mixins.cloud_mixin import CloudMixin
from deploy.common.mixins.bashrc_mixin import BashrcMixin

class ServerDeployer(BaseDeployer, DockerMixin, CloudMixin, BashrcMixin):
    IMAGE_NAME = "server-engine"
    DOCKERFILE = "cloud/Docker/server/server.Dockerfile"
    CONTEXT = "server"
    TAG = "gcr.io/my-project/server-engine:1.0.0"

    def setup_os_env(self):
        self.setup_bashrc(node=False, poetry=True)
