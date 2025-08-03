import subprocess

class CloudMixin:
    def cloud_deploy(self, image_name: str, tag: str):
        print(f"[CloudMixin] Deploying {image_name} to {tag}...")
        subprocess.run(
            ["gcloud", "builds", "submit", ".", "--tag", tag],
            check=True,
        )
        subprocess.run(
            ["gcloud", "run", "deploy", image_name,
             "--image", tag,
             "--platform", "managed"],
            check=True,
        )
