import os
from util.env import load_server_env, load_providers_env


load_server_env()
load_providers_env()


class Deployment:
    _deployment = os.getenv("DEPLOYMENT")
    _deployment_env = os.getenv("DEPLOYMENT_ENV")

    @property
    def deployment(self):
        return self._deployment

    @property
    def deployment_env(self):
        return self._deployment_env
