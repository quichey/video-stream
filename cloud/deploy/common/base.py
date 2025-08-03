from abc import ABC, abstractmethod
import os

class BaseDeployer(ABC):
    def deploy(self):
        print(f"=== Deploying {self.__class__.__name__} ===")
        self.setup_os_env()
        self.build_docker_image()
        self.launch_instance()

    @abstractmethod
    def setup_os_env(self):
        pass

    def is_cloud(self) -> bool:
        return os.environ.get("DEPLOY_ENV", "local") == "cloud"

    #
    # Subclasses must provide these as class attributes:
    # IMAGE_NAME, DOCKERFILE, CONTEXT, TAG
    #

    def build_docker_image(self):
        """Unified method for building Docker images (cloud or local)."""
        if self.is_cloud():
            print(f"[BaseDeployer] Cloud build for {self.IMAGE_NAME}")
            self.build_docker_image_cloud(
                image_name=self.IMAGE_NAME,
                dockerfile=self.DOCKERFILE,
                context=self.CONTEXT,
                tag=self.TAG,
            )
        else:
            print(f"[BaseDeployer] Local build for {self.IMAGE_NAME}")
            self.build_docker_image_local(
                image_name=self.IMAGE_NAME,
                dockerfile=self.DOCKERFILE,
                context=self.CONTEXT,
            )

    def launch_instance(self):
        """Unified method for launching Docker images (cloud or local)."""
        if self.is_cloud():
            self.cloud_deploy(
                image_name=self.IMAGE_NAME,
                tag=self.TAG,
            )
        else:
            self.docker_run(
                image_name=self.IMAGE_NAME,
                port=8080,
            )
