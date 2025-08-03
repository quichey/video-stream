import subprocess
from pathlib import Path

class PackageManagerMixin:
    def install_node_packages(self, path: str = "client"):
        """Run npm install in the given directory."""
        print(f"[PackageManagerMixin] Installing Node packages in {path}...")
        subprocess.run(["npm", "install"], cwd=path, check=True)

    def install_poetry_packages(self, path: str = "server"):
        """Run poetry install in the given directory."""
        print(f"[PackageManagerMixin] Installing Poetry packages in {path}...")
        lock_file = Path(path) / "poetry.lock"
        # Ensure lock file exists before install
        if not lock_file.exists():
            print(f"[PackageManagerMixin] No poetry.lock found, generating...")
            subprocess.run(["poetry", "lock"], cwd=path, check=True)
        subprocess.run(["poetry", "install"], cwd=path, check=True)
