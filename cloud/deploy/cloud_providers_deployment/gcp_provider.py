from dotenv import load_dotenv
from typing_extensions import override
import os

from .base_provider import BaseCloudProvider

load_dotenv()

class GoogleCloudProvider(BaseCloudProvider):
    def __init__(self, context):
        super().__init__(context=context)
        self.image.base_tag = f"gcr.io/my-project/{context}-engine"
        return


    @override
    def get_latest_image(self, image_tag_base, repo_name):
        pass

    @override
    def get_build_cmd(self, dockerfile, package_path):
        return [
            "gcloud", "builds", "submit", package_path,
            "--tag", self.image.full_tag,
            "--gcs-log-dir", "gs://my-logs"  # optional
        ]

    @override
    def get_run_cmd(self):
        return [
            "gcloud", "run", "deploy", self.image.name,
            "--image", self.image.full_tag,
            "--platform", "managed",
        ]

