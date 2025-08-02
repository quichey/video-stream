import subprocess
import os

class BaseDeployer:
    def __init__(self, root_dir: str, env: str):
        self.root_dir = root_dir
        self.env = env  # "local" or "cloud"

    def run_cmd(self, cmd, cwd=None):
        """Run a shell command."""
        print(f"[RUNNING] {cmd}")
        subprocess.run(cmd, cwd=cwd, shell=True, check=True)

    def setup_env(self):
        """Base environment setup."""
        print(f"[INFO] Setting up environment for {self.env}...")
        # OS detection could be added here
        # Could source .bashrc.local or .bashrc.cloud if needed

    def build(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
