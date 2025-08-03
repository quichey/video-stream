import subprocess

class CloudMixin:
    def build_docker_image_cloud(self, image_name: str, dockerfile: str, context: str, tag: str):
        print(f"[CloudMixin] Building and submitting cloud image {image_name}")
        # Submit cloud build
        subprocess.run(
            [
                "gcloud", "builds", "submit", context,
                "--tag", tag,
                "--gcs-log-dir", "gs://my-logs"  # optional
            ],
            check=True,
        )

    def cloud_deploy(self, image_name: str, tag: str):
        print(f"[CloudMixin] Deploying {image_name} to Cloud Run...")
        subprocess.run(
            [
                "gcloud", "run", "deploy", image_name,
                "--image", tag,
                "--platform", "managed",
            ],
            check=True,
        )
