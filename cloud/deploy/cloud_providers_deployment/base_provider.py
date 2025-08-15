from abc import ABC, abstractmethod

from common.dataclass_models.image import Image

class BaseCloudProvider(ABC):
    def __init__(self, context):
        self._context = context
        self._image = Image(name=f"{context}-engine")

    @property
    def context(self):
        return self._context

    @property
    @abstractmethod
    def repo_name(self):
        return self._repo_name

    @repo_name.setter
    def repo_name(self, new_value):
        self._repo_name = new_value

    @property
    @abstractmethod
    def image(self) -> Image:
        return self._image

    @abstractmethod
    def get_latest_image(self, image_tag_base, repo_name):
        pass

    @abstractmethod
    def get_build_cmd(self, dockerfile, package_path, tag):
        pass

    @abstractmethod
    def get_run_cmd(self, image_name, tag):
        pass