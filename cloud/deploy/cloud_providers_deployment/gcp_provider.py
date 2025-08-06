from dotenv import load_dotenv
import os

from .base_provider import BaseCloudProvider

load_dotenv()

class GoogleCloudProvider(BaseCloudProvider):
    def __init__(self, context):
        self.image_name = f"{context}-engine"
        self.tag = f"gcr.io/my-project/{context}-engine:1.0.0"
        return

    def get_build_cmd(self, dockerfile, package_path):
        return [
            "gcloud", "builds", "submit", package_path,
            "--tag", self.tag,
            "--gcs-log-dir", "gs://my-logs"  # optional
        ]

    def get_run_cmd(self):
        return [
            "gcloud", "run", "deploy", self.image_name,
            "--image", self.tag,
            "--platform", "managed",
        ]

