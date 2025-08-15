from dotenv import load_dotenv
from typing_extensions import override
import os

from .base_provider import BaseCloudProvider

load_dotenv()

class GoogleCloudProvider(BaseCloudProvider):
    def __init__(self, context):
        super().__init__(context=context)
        self.image_name = f"{context}-engine"
        self.tag = f"gcr.io/my-project/{context}-engine:1.0.0"
        return

    @property
    @override
    def repo_name(self):
        pass

    @property
    @override
    def image_tag_base(self):
        pass

    @property
    @override
    def tag(self):
        return f"gcr.io/my-project/{self.context}-engine:1.0.0"

    @override
    def get_latest_image(self, image_tag_base, repo_name):
        pass

    @override
    def get_build_cmd(self, dockerfile, package_path, tag):
        return [
            "gcloud", "builds", "submit", package_path,
            "--tag", tag,
            "--gcs-log-dir", "gs://my-logs"  # optional
        ]

    @override
    def get_run_cmd(self):
        return [
            "gcloud", "run", "deploy", self.image_name,
            "--image", self.tag,
            "--platform", "managed",
        ]

