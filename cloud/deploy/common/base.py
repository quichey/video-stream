from pathlib import Path
import subprocess
from abc import ABC, abstractmethod

class BaseDeployer(ABC):
    def __init__(self, project_root: str, deploy_env: str):
        self.project_root = Path(project_root)
        self.deploy_env = deploy_env  # "local" or "cloud"

    def run_cmd(self, cmd: str):
        print(f"[RUNNING] {cmd}")
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {cmd}")

    def deploy(self):
        self.setup_os_env()
        self.build_docker_image()
        self.launch_instance()

    @abstractmethod
    def setup_os_env(self):
        """Prepare the OS environment, e.g., install deps, set env variables"""
        pass

    @abstractmethod
    def build_docker_image(self):
        """Build any required Docker images"""
        pass

    @abstractmethod
    def launch_instance(self):
        """Run locally or deploy to cloud"""
        pass
