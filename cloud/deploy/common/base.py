from abc import ABC, abstractmethod
import shutil
import os

class BaseDeployer(ABC):
    PATH_PROJECT_ROOT = "../.."
    PATH_PROJECT_DOCKER = "../Docker"
    def deploy(self):
        print(f"=== Deploying {self.__class__.__name__} ===")
        self.verify_os_env()
        self.bundle_packages()
        self.build_docker_image()
        self.launch_instance()

    def verify_os_env(self):
        """Shared OS environment verification based on package_manager."""
        if self.PACKAGE_MANAGER == "npm":
            for tool in ["node", "npm"]:
                if shutil.which(tool) is None:
                    raise EnvironmentError(f"{tool} not found. Run deploy/os/linux/env_setup.sh first.")
        elif self.PACKAGE_MANAGER == "poetry":
            if shutil.which("poetry") is None:
                raise EnvironmentError("poetry not found. Run deploy/os/linux/env_setup.sh first.")
        else:
            raise ValueError(f"Unknown package manager: {self.PACKAGE_MANAGER}")

    def bundle_packages(self):
        """Shared package installation."""
        if self.PACKAGE_MANAGER == "npm":
            self.install_node_packages(path=self.PACKAGE_PATH)
        elif self.PACKAGE_MANAGER == "poetry":
            self.install_poetry_packages(path=self.PACKAGE_PATH)
        else:
            raise ValueError(f"Unknown package manager: {self.PACKAGE_MANAGER}")

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
                package_path=self.PACKAGE_PATH,
                tag=self.TAG,
            )
        else:
            print(f"[BaseDeployer] Local build for {self.IMAGE_NAME}")
            self.build_docker_image_local(
                image_name=self.IMAGE_NAME,
                dockerfile=self.DOCKERFILE,
                package_path=self.PACKAGE_PATH,
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