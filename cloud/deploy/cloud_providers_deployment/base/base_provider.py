from abc import ABC
import shutil
from pathlib import Path

from common.dataclasses_models.image import Image


class BaseCloudProvider(ABC):
    PROVIDER_NAME = ""

    def __init__(self, context, env):
        self._context = context
        repository = f"{context}-engine" if env == "prod" else f"{context}-engine-{env}"
        self._image = Image(registry="unkown", repository=repository, tag="1.0.0")

    @property
    def context(self):
        return self._context

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
