import subprocess
from pathlib import Path
import shutil

class DockerMixin:
    def get_latest_image(self):
        prefix = "my-prefix"
        result = subprocess.run(
            ["docker", "images", "--format", "{{.Repository}}"],
            capture_output=True,
            text=True
        )
        images = [name for name in result.stdout.splitlines() if name.startswith(prefix)]
        return images[0]

    def build_docker_image_local(self, image_name: str, dockerfile: str, package_path: str):
        """
        Builds a Docker image using the specified Dockerfile and context.
        Automatically copies .dockerignore from the Dockerfile's directory into the context.

        :param image_name: name:tag for the image
        :param dockerfile: path to Dockerfile
        :param package_path: path to build context (where Docker will look for .dockerignore)
        """
        package_path = Path(package_path).resolve()
        dockerfile_path = Path(dockerfile).resolve()
        dockerfile_dir = dockerfile_path.parent

        if not package_path.exists():
            raise FileNotFoundError(f"Build context path does not exist: {package_path}")
        if not dockerfile_path.exists():
            raise FileNotFoundError(f"Dockerfile does not exist: {dockerfile_path}")

        # Copy .dockerignore from Dockerfile directory to build context if it exists
        dockerignore_src = dockerfile_dir / ".dockerignore"
        dockerignore_dst = package_path / ".dockerignore"
        if dockerignore_src.exists():
            shutil.copy2(dockerignore_src, dockerignore_dst)
            print(f"[DockerMixin] Copied .dockerignore from {dockerignore_src} to {dockerignore_dst}")
        else:
            print(f"[DockerMixin] No .dockerignore found at {dockerignore_src}, skipping copy")

        print(f"[DockerMixin] Building image {image_name} using context {package_path} and Dockerfile {dockerfile_path}")
        subprocess.run(
            ["docker", "build", "-t", image_name, "-f", str(dockerfile_path), str(package_path)],
            check=True,
        )

    def docker_run(self, image_name: str, port: int = 8080):
        print(f"[DockerMixin] Running image {image_name} locally on port {port}...")
        subprocess.run(
            ["docker", "run", "-d", "-p", f"{port}:{port}", image_name],
            check=True,
        )
