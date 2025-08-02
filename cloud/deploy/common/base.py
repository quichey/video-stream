import abc
import subprocess
from pathlib import Path
from os.linux import env_setup

class BaseDeployer(abc.ABC):
    """Abstract base class for deployers."""

    def __init__(self, name: str, base_dir: Path):
        self.name = name
        self.base_dir = base_dir
        self.env = env_setup.detect_environment()

    def run_cmd(self, cmd: str):
        print(f"[{self.name}] Running: {cmd}")
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            raise RuntimeError(f"{self.name} command failed: {cmd}")

    def setup_bashrc(self):
        """Default bashrc setup – subclasses may override."""
        print(f"[{self.name}] Detected environment: {self.env}")
        bashrc_file = f"os/linux/.bashrc.{self.env}.example"
        print(f"[{self.name}] (Optional) Load config from {bashrc_file}")

    @abc.abstractmethod
    def setup(self):
        ...

    @abc.abstractmethod
    def build(self):
        ...

    @abc.abstractmethod
    def run(self):
        ...

    def deploy(self):
        print(f"=== Deploying {self.name} ===")
        self.setup_bashrc()
        self.setup()
        self.build()
        self.run()
        print(f"=== Finished {self.name} ===")
