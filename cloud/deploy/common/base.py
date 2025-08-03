from abc import ABC, abstractmethod

class BaseDeployer(ABC):
    def deploy(self):
        print(f"=== Deploying {self.__class__.__name__} ===")
        self.setup_os_env()
        self.build_docker_image()
        self.launch_instance()

    @abstractmethod
    def setup_os_env(self):
        pass

    @abstractmethod
    def build_docker_image(self):
        pass

    @abstractmethod
    def launch_instance(self):
        pass
