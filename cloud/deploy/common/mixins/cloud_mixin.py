import subprocess

from cloud_providers_deployment import get_provider_class

class CloudMixin:
    def __init__(self, provider_name, **kwargs):
        self.provider = get_provider_class(provider_name)()
        self.acr_name=kwargs["acr_name"]
        self.resource_group=kwargs["resource_group"]
        self.environment_name=kwargs["environment_name"]

    def build_docker_image_cloud(self, image_name: str, dockerfile: str, package_path: str, tag: str):
        cloud_cmd = self.provider.get_build_cmd(
            dockerfile,
            package_path,
            tag,
            acr_name=self.acr_name,
        )
        print(f"[CloudMixin] Building and submitting cloud image {image_name}")
        # Submit cloud build
        subprocess.run(
            cloud_cmd,
            check=True,
        )

    def cloud_deploy(self, image_name: str, tag: str):
        cloud_cmd = self.provider.get_run_cmd(
            image_name,
            tag,
            acr_name=self.acr_name,
            resource_group=self.resource_group,
            environment_name=self.environment_name,
        )
        print(f"[CloudMixin] Deploying {image_name} to Cloud Run...")
        subprocess.run(
            cloud_cmd,
            check=True,
        )
