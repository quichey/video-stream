from abc import ABC, abstractmethod

from common.dataclasses_models.image import Image

class BaseCloudProvider(ABC):
    def __init__(self, context):
        self._context = context
        self._image = Image(registry="unkown", repository=f"{context}-engine", tag='1.0.0')

    @property
    def context(self):
        return self._context

    @property
    def image(self) -> Image:
        return self._image

    @abstractmethod
    def get_latest_image_cmd(self):
        pass

    @abstractmethod
    def get_build_cmd(self, dockerfile, package_path):
        pass

    @abstractmethod
    def get_run_cmd(self):
        pass