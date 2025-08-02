from common.base import BaseDeployer
from pathlib import Path

class ServerDeployer(BaseDeployer):
    def setup_os_env(self):
        bashrc_file = self.project_root / "deploy" / "os" / "linux" / (
            ".bashrc.cloud.example" if self.deploy_env == "cloud" else ".bashrc.local.example"
        )
        print(f"Appending {bashrc_file} to ~/.bashrc")
        with open(bashrc_file) as src, open(Path.home() / ".bashrc", "a") as dest:
            dest.write("\n# ServerDeployer setup\n")
            dest.write(src.read())

        print("Installing Python dependencies...")
        self.run_cmd("pip install poetry")
        self.run_cmd("poetry install")

    def build_docker_image(self):
        print("Building server Docker image...")
        self.run_cmd(
            "docker build -t server-engine-dev -f cloud/Docker/server/server.Dockerfile server"
        )

    def launch_instance(self):
        if self.deploy_env == "cloud":
            print("Deploying server to Cloud Run...")
            self.run_cmd(
                "gcloud run deploy server-service "
                "--source server "
                "--region us-central1 "
                "--allow-unauthenticated"
            )
        else:
            print("Running server locally...")
            self.run_cmd("poetry run python server/main.py")
