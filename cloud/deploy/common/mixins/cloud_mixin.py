from util.subprocess_helper import run_cmds

from cloud_providers_deployment import get_provider_class

class CloudMixin:
    def __init__(self, provider_name, context):
        self.context = context
        self.provider = get_provider_class(provider_name)(context)

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
        run_cmds(
            cloud_cmd,
            check=True,
        )
