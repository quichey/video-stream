from pathlib import Path
from common.base import BaseDeployer

class ClientDeployer(BaseDeployer):
    def __init__(self):
        super().__init__("Client", Path(__file__).resolve().parents[1] / "client")

    def setup_bashrc(self):
        super().setup_bashrc()
        if self.env == "cloud":
            print("[Client] Cloud shell: ensuring Node.js & npm installed")
            # e.g., self.run_cmd("sudo apt-get update && sudo apt-get install -y nodejs npm")
        else:
            print("[Client] Local: using system Node.js/npm")

    def setup(self):
        self.run_cmd("npm install")

    def build(self):
        self.run_cmd("npm run build")

    def run(self):
        self.run_cmd("docker build -t client-engine-dev -f ../Docker/client/client.Dockerfile .")
