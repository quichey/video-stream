import subprocess
from pathlib import Path

class BashrcMixin:
    def setup_bashrc(self, node=False, poetry=False):
        bashrc = Path.home() / ".bashrc"
        print(f"[BashrcMixin] Configuring {bashrc}...")

        if node:
            subprocess.run(["apt-get", "update"], check=True)
            subprocess.run(["apt-get", "install", "-y", "nodejs", "npm"], check=True)
        if poetry:
            subprocess.run(["pip", "install", "--upgrade", "pip"], check=True)
            subprocess.run(["pip", "install", "poetry"], check=True)

        with open(bashrc, "a") as f:
            f.write("\n# Added by deployer\nexport DEPLOY_ENV=cloud\n")
