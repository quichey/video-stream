from .base_provider import BaseCloudProvider

class GoogleCloudProvider(BaseCloudProvider):
    def get_build_cmd(self, dockerfile, package_path, tag):
        return [
            "gcloud", "builds", "submit", package_path,
            "--tag", tag,
            "--gcs-log-dir", "gs://my-logs"  # optional
        ]

    def get_run_cmd(self, image_name, tag):
        return [
            "gcloud", "run", "deploy", image_name,
            "--image", tag,
            "--platform", "managed",
        ]

