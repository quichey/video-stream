from abc import ABC, abstractmethod

from common.dataclasses_models.image import Image
from cloud_providers_deployment.base.base_provider import BaseCloudProvider


class BaseCloudContainerProvider(BaseCloudProvider, ABC):
    def __init__(self, context, env):
        super().__init__(context, env)
        repository = f"{context}-engine" if env == "prod" else f"{context}-engine-{env}"
        self._image = Image(registry="unkown", repository=repository, tag="1.0.0")

    @property
    def context(self):
        return self._context

    @property
    def image(self) -> Image:
        return self._image

    @abstractmethod
    def get_container_url(self):
        pass

    @abstractmethod
    def get_latest_image_cmd(self):
        pass

    @abstractmethod
    def get_build_cmd(self, dockerfile, package_path):
        pass

    @abstractmethod
    def get_run_cmd(self):
        pass
