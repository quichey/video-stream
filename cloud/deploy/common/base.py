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
        # Could also check ENV vars like GOOGLE_CLOUD_PROJECT
        return os.environ.get("DEPLOY_ENV", "local") == "cloud"

    @abstractmethod
    def build_docker_image(self):
        pass

    @abstractmethod
    def launch_instance(self):
        pass
