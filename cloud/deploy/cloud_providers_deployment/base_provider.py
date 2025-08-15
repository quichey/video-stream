from abc import ABC, abstractmethod

class BaseCloudProvider(ABC):
    def __init__(self, context):
        self._context = context

    @property
    def context(self):
        return self._context

    @property
    @abstractmethod
    def repo_name(self):
        pass

    @property
    @abstractmethod
    def image_tag_base(self):
        pass

    @property
    @abstractmethod
    def repo_name(self):
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