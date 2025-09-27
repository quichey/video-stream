from abc import ABC, abstractmethod
import shutil
from pathlib import Path

from common.dataclasses_models.image import Image
from cloud_providers_deployment.base.base_provider import BaseCloudProvider


class BaseCloudContainerProvider(BaseCloudProvider, ABC):
    def __init__(self, context, env):
        self._context = context
        repository = f"{context}-engine" if env == "prod" else f"{context}-engine-{env}"
        self._image = Image(registry="unkown", repository=repository, tag="1.0.0")

    @property
    def context(self):
        return self._context

    @property
    def image(self) -> Image:
        return self._image

    """
    Copy over cloud/providers/<name>/.env to <service>/env/<name>/.env?
    """

    def set_up_env(self):
        source = f"../providers/{self.PROVIDER_NAME}/.env"
        dest = f"../../{self.context}/env/{self.PROVIDER_NAME}"
        dst_dir = Path(dest)
        dst_dir.mkdir(parents=True, exist_ok=True)  # create dirs if missing
        shutil.copy(source, dest)
        return

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
