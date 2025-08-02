from pathlib import Path
from common.base import BaseDeployer

class ServerDeployer(BaseDeployer):
    def __init__(self):
        super().__init__("Server", Path(__file__).resolve().parents[1] / "server")

    def setup_bashrc(self):
        super().setup_bashrc()
        if self.env == "cloud":
            print("[Server] Cloud shell: ensuring Python and Poetry installed")
            # Example:
            # self.run_cmd("sudo apt-get update && sudo apt-get install -y python3-pip")
            # self.run_cmd("pip install poetry")
        else:
            print("[Server] Local: using system Python/Poetry")

    def setup(self):
        self.run_cmd("poetry install")

    def build(self):
        print("Server build step (placeholder)")

    def run(self):
        self.run_cmd("poetry run python main.py")
