import os
import sys

from util.env import load_server_env, load_providers_env


load_server_env()
load_providers_env()


class Deployment:
    _deployment = os.getenv("DEPLOYMENT")
    _deployment_env = os.getenv("DEPLOYMENT_ENV")

    @property
    def deployment(self):
        return os.getenv("DEPLOYMENT")

    @property
    def deployment_env(self):
        return os.getenv("DEPLOYMENT_ENV")

    def log(self, print_text: str):
        if self.deployment in ["local", "test"]:
            return print(print_text)
        elif self.deployment == "cloud":
            return print(print_text, file=sys.stderr, flush=True)
