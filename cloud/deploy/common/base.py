from abc import ABC, abstractmethod
from dotenv import load_dotenv
import shutil
import os

from common.mixins.package_manager_mixin import PackageManagerMixin
from common.mixins.docker_mixin import DockerMixin
from common.mixins.cloud_mixin import CloudMixin
from common.mixins.bashrc_mixin import BashrcMixin
from common.mixins.version_mixin import VersionMixin

from common.dataclass_models.image import Image

load_dotenv()

class BaseDeployer(ABC, PackageManagerMixin, DockerMixin, BashrcMixin, VersionMixin):
    PATH_PROJECT_ROOT = "../.."
    PATH_PROJECT_DOCKER = "../Docker"

    def __init__(self, provider_name):
        if self.is_cloud():
            self.cloud_mixin_instance = CloudMixin(
                provider_name=provider_name,
                context=self.CONTEXT
            )
            self.provider = self.cloud_mixin_instance.provider
            self.image = self.provider.image
        else:
            local_image_name = f"{self.CONTEXT}-engine"
            self.image = Image(name=local_image_name, base_tag=f"local-{provider_name}-{local_image_name}")

    def deploy(self):
        print(f"=== Deploying {self.__class__.__name__} ===")
        self.verify_os_env()
        self.bundle_packages()
        self.generate_new_image_tag()
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

    def generate_new_image_tag(self):
        if self.is_cloud():
            print(f"[BaseDeployer] Generating Latest Image Tag {self.CONTEXT}")
            repo_name = self.provider.repo_name
            image_tag_base = self.image.base_tag
            new_tag = self.generate_timestamped_tag(image_tag_base=image_tag_base, repo_name=repo_name)
            self.image.full_tag = new_tag
        else:
            repo_name = pass
            image_tag_base = self.image.base_tag
            new_tag = self.generate_timestamped_tag(image_tag_base=image_tag_base, repo_name=repo_name)
            self.image.full_tag = new_tag
        return

    #
    # Subclasses must provide these as class attributes:
    # IMAGE_NAME, DOCKERFILE, CONTEXT, TAG
    #

    def build_docker_image(self):
        """Unified method for building Docker images (cloud or local)."""
        if self.is_cloud():
            print(f"[BaseDeployer] Cloud build for {self.CONTEXT}")
            self.cloud_mixin_instance.build_docker_image_cloud(
                dockerfile=self.DOCKERFILE,
                package_path=self.PACKAGE_PATH,
            )
        else:
            print(f"[BaseDeployer] Local build for {self.CONTEXT}")
            self.build_docker_image_local(
                image_name=self.CONTEXT,
                dockerfile=self.DOCKERFILE,
                package_path=self.PACKAGE_PATH,
            )

    def launch_instance(self):
        """Unified method for launching Docker images (cloud or local)."""
        if self.is_cloud():
            self.cloud_mixin_instance.cloud_deploy()
        else:
            machine_context = self.CONTEXT.upper()
            port =  os.environ.get(f"PORT_{machine_context}", "local")
            self.docker_run(
                image_name=self.CONTEXT,
                port=port,
            )