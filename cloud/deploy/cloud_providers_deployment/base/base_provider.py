from abc import ABC
import shutil
from pathlib import Path


class BaseCloudProvider(ABC):
    PROVIDER_NAME = ""

    def __init__(self, context, env):
        self._context = context
        self._env = env

    @property
    def context(self):
        return self._context

    @property
    def env(self):
        return self._env

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
