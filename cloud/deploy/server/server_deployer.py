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

    def build_docker_image(self):
        if self.is_cloud():
            self.build_docker_image_cloud(
                image_name=self.IMAGE_NAME,
                dockerfile=self.DOCKERFILE,
                context=self.CONTEXT,
                tag=self.TAG,
            )
        else:
            self.build_docker_image_local(
                image_name=self.IMAGE_NAME,
                dockerfile=self.DOCKERFILE,
                context=self.CONTEXT,
            )

    def launch_instance(self):
        if self.is_cloud():
            self.cloud_deploy(
                image_name=self.IMAGE_NAME,
                tag=self.TAG,
            )
        else:
            self.docker_run(image_name=self.IMAGE_NAME, port=8080)
