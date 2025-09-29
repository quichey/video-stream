import re

from util.subprocess_helper import run_cmds, run_cmd_with_retries
from common.mixins.cloud_mixin.cloud_mixin import CloudMixin

from cloud_providers_deployment import get_provider_class_container


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


class CloudContainerMixin(CloudMixin):
    GET_PROVIDER_CLASS_FUNC = get_provider_class_container

    def get_images_archives(self):
        """
        Fetch the latest semantic version tag from ACR.
        Returns "0.0.0" if no valid tags are found.
        """
        latest_image_cmd = self.provider.get_latest_image_cmd()
        result = run_cmds(latest_image_cmd, capture_output=True, text=True)
        if not result:
            return []
        else:
            # print(f"\n\n result: {result} \n\n")
            # for r in result:
            #    print(f"\n\n r: {r} \n\n")
            return [
                t
                for t in result.stdout.strip().split("\n")
                if re.match(
                    r"^\d+\.\d+\.\d+(-dev-\d{4}-\d{2}-\d{2}--\d{2}-\d{2}-\d{2})?$", t
                )
            ]

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
