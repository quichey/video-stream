from deploy.common.base import BaseDeployer
from deploy.common.mixins.docker_mixin import DockerMixin
from deploy.common.mixins.cloud_mixin import CloudMixin
from deploy.common.mixins.bashrc_mixin import BashrcMixin

class ClientDeployer(BaseDeployer, DockerMixin, CloudMixin, BashrcMixin):
    def setup_os_env(self):
        self.setup_bashrc(node=True, poetry=False)

    def build_docker_image(self):
        self.docker_build(
            image_name="client-engine",
            dockerfile="cloud/Docker/client/client.Dockerfile",
            context="client"
        )

    def launch_instance(self):
        self.cloud_deploy(
            image_name="client-engine",
            tag="gcr.io/my-project/client-engine:1.0.0"
        )
