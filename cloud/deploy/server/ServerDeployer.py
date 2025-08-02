import os
from common.base import BaseDeployer

class ServerDeployer(BaseDeployer):
    def __init__(self, root_dir, env):
        super().__init__(root_dir, env)
        self.server_dir = os.path.join(self.root_dir, "server")

    def build(self):
        print("[SERVER] Installing Python dependencies...")
        self.run_cmd("poetry install", cwd=self.server_dir)

    def run(self):
        print("[SERVER] Running Python server...")
        self.run_cmd("poetry run python main.py", cwd=self.server_dir)
