from datetime import datetime
import re

from util.subprocess_helper import run_cmds, run_cmd_with_retries

from cloud_providers_deployment import get_provider_class

def pre_build_hook(func):
    """Decorator to run a pre-build step if the subclass/provider defines it."""
    def wrapper(self, *args, **kwargs):
        # Call pre-build step if provider has it
        pre_build = getattr(self.provider, "pre_build_image_cloud", None)
        if callable(pre_build):
            print(f"[CloudMixin] Running pre-build step for {self.context}...")
            pre_build(*args, **kwargs)
        return func(self, *args, **kwargs)
    return wrapper

class CloudMixin:
    def __init__(self, provider_name, context):
        self.context = context
        self.provider = get_provider_class(provider_name)(context)

    @pre_build_hook
    def build_docker_image_cloud(self, dockerfile: str, package_path: str):
        cloud_cmd = self.provider.get_build_cmd(
            dockerfile,
            package_path,
        )
        print(f"[CloudMixin] Building and submitting cloud image {self.context}")
        # Submit cloud build
        run_cmds(
            cloud_cmd,
            check=True,
        )

    def cloud_deploy(self):
        cloud_cmd = self.provider.get_run_cmd()
        print(f"[CloudMixin] Deploying {self.context} to Cloud Run...")
        run_cmd_with_retries(
            cloud_cmd,
            check=True,
        )
