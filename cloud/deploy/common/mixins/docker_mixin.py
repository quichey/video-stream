import subprocess

class DockerMixin:
    def build_docker_image_local(self, image_name: str, dockerfile: str, context: str):
        print(f"[DockerMixin] Building image locally: {image_name}")
        subprocess.run(
            ["docker", "build", "-t", image_name, "-f", dockerfile, context],
            check=True,
        )

    def docker_run(self, image_name: str, port: int = 8080):
        print(f"[DockerMixin] Running image {image_name} locally...")
        subprocess.run(
            ["docker", "run", "-p", f"{port}:{port}", image_name],
            check=True,
        )
