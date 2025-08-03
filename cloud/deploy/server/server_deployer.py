from deploy.common.base import BaseDeployer
from deploy.common.mixins.docker_mixin import DockerMixin
from deploy.common.mixins.cloud_mixin import CloudMixin
from deploy.common.mixins.bashrc_mixin import BashrcMixin

class ServerDeployer(BaseDeployer, DockerMixin, CloudMixin, BashrcMixin):
    def setup_os_env(self):
        self.setup_bashrc(node=False, poetry=True)

    def build_docker_image(self):
        self.docker_build(
            image_name="server-engine",
            dockerfile="cloud/Docker/server/server.Dockerfile",
            context="server"
        )

    def launch_instance(self):
        self.cloud_deploy(
            image_name="server-engine",
            tag="gcr.io/my-project/server-engine:1.0.0"
        )
