import os
from common.base import BaseDeployer

class ClientDeployer(BaseDeployer):
    def __init__(self, root_dir, env):
        super().__init__(root_dir, env)
        self.client_dir = os.path.join(self.root_dir, "client")

    def build(self):
        print("[CLIENT] Building React app...")
        self.run_cmd("npm install", cwd=self.client_dir)
        self.run_cmd("npm run build", cwd=self.client_dir)

    def run(self):
        print("[CLIENT] Running Docker container...")
        dockerfile = os.path.join(self.root_dir, "cloud/Docker/client/client.Dockerfile")
        self.run_cmd(f"docker build -t client-engine-dev -f {dockerfile} {self.client_dir}")
