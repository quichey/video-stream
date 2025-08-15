from abc import ABC, abstractmethod

class BaseCloudProvider(ABC):
    @abstractmethod
    def get_repo_name(self):
        pass

    @abstractmethod
    def get_image_tag_base(self, repo_name):
        pass

    @abstractmethod
    def get_latest_image(self, image_tag_base, repo_name):
        pass

    @abstractmethod
    def get_build_cmd(self, dockerfile, package_path, tag):
        pass

    @abstractmethod
    def get_run_cmd(self, image_name, tag):
        pass