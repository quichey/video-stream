from abc import ABC, abstractmethod
import shutil
import os

class BaseDeployer(ABC):
    def deploy(self):
        print(f"=== Deploying {self.__class__.__name__} ===")
        self.verify_os_env()
        self.bundle_packages()
        self.build_docker_image()
        self.launch_instance()

    def verify_os_env(self):
        """Shared OS environment verification based on package_manager."""
        if self.package_manager == "npm":
            for tool in ["node", "npm"]:
                if shutil.which(tool) is None:
                    raise EnvironmentError(f"{tool} not found. Run deploy/os/linux/env_setup.sh first.")
        elif self.package_manager == "poetry":
            if shutil.which("poetry") is None:
                raise EnvironmentError("poetry not found. Run deploy/os/linux/env_setup.sh first.")
        else:
            raise ValueError(f"Unknown package manager: {self.package_manager}")

    def bundle_packages(self):
        """Shared package installation."""
        if self.package_manager == "npm":
            self.install_node_packages(path=self.package_path)
        elif self.package_manager == "poetry":
            self.install_poetry_packages(path=self.package_path)
        else:
            raise ValueError(f"Unknown package manager: {self.package_manager}")

    def is_cloud(self) -> bool:
        return os.environ.get("DEPLOY_ENV", "local") == "cloud"

    #
    # Subclasses must provide these as class attributes:
    # IMAGE_NAME, DOCKERFILE, CONTEXT, TAG
    #

    def build_docker_image(self):
        """Unified method for building Docker images (cloud or local)."""
        if self.is_cloud():
            print(f"[BaseDeployer] Cloud build for {self.IMAGE_NAME}")
            self.build_docker_image_cloud(
                image_name=self.IMAGE_NAME,
                dockerfile=self.DOCKERFILE,
                context=self.CONTEXT,
                tag=self.TAG,
            )
        else:
            print(f"[BaseDeployer] Local build for {self.IMAGE_NAME}")
            self.build_docker_image_local(
                image_name=self.IMAGE_NAME,
                dockerfile=self.DOCKERFILE,
                context=self.CONTEXT,
            )

    def launch_instance(self):
        """Unified method for launching Docker images (cloud or local)."""
        if self.is_cloud():
            self.cloud_deploy(
                image_name=self.IMAGE_NAME,
                tag=self.TAG,
            )
        else:
            self.docker_run(
                image_name=self.IMAGE_NAME,
                port=8080,
            )