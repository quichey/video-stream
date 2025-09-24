import re

from util.subprocess_helper import run_cmds, run_cmd_with_retries, CloudError

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
    def __init__(self, provider_name, context, env):
        self.context = context
        self.provider = get_provider_class(provider_name)(context, env)

    def set_up_provider_env(self):
        self.provider.set_up_env()
        return

    def is_first_deployment(self) -> bool:
        """
        Fetch the latest semantic version tag from ACR.
        Returns "0.0.0" if no valid tags are found.
        """
        try:
            latest_image_cmd = self.provider.get_latest_image_cmd()
            result = run_cmds(latest_image_cmd, capture_output=True, text=True)
            if len(result) > 0:
                return False
            else:
                return True
        except CloudError:
            return True

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

    def start(self):
        cloud_cmd = self.provider.get_start_cmd()
        print(f"[CloudMixin] Starting up {self.context}...")
        run_cmd_with_retries(
            cloud_cmd,
            check=True,
        )

    def stop(self):
        cloud_cmd = self.provider.get_stop_cmd()
        print(f"[CloudMixin] Stopping {self.context}...")
        run_cmd_with_retries(
            cloud_cmd,
            check=True,
        )

    def restart(self):
        cloud_cmd = self.provider.get_restart_cmd()
        print(f"[CloudMixin] Restarting {self.context}...")
        run_cmd_with_retries(
            cloud_cmd,
            check=True,
        )
