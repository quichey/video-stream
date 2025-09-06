import os
from util.env import load_server_env, load_providers_env


load_server_env()
load_providers_env()


class Deployment:
    _deployment = os.getenv("DEPLOYMENT")

    @property
    def deployment(self):
        return self._deployment
