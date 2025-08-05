from abc import ABC, abstractmethod

class BaseCloudProvider(ABC):
    @abstractmethod
    def get_build_cmd(self, dockerfile, package_path, tag):
        pass

    @abstractmethod
    def get_run_cmd(self, image_name, tag):
        pass