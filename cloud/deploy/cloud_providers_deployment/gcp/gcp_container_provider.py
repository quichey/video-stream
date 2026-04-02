from dotenv import load_dotenv
from typing_extensions import override

from cloud_providers_deployment.base.base_container_provider import (
    BaseCloudContainerProvider,
)

load_dotenv()


class GoogleCloudContainerProvider(BaseCloudContainerProvider):
    PROVIDER_NAME = "gcp"

    def __init__(self, context, env):
        super().__init__(context, env)
        self.image.registry = "gcr.io/my-project"
        return

    @override
    def get_latest_image_cmd(self):
        pass

    @override
    def get_build_cmd(self, dockerfile, package_path):
        return [
            "gcloud",
            "builds",
            "submit",
            package_path,
            "--tag",
            self.image.full_name,
            "--gcs-log-dir",
            "gs://my-logs",  # optional
        ]

    @override
    def get_run_cmd(self):
        return [
            "gcloud",
            "run",
            "deploy",
            self.image.repository,
            "--image",
            self.image.full_name,
            "--platform",
            "managed",
        ]
