from abc import ABC, abstractmethod
from dotenv import load_dotenv
import shutil
import os

from common.mixins.package_manager_mixin import PackageManagerMixin
from common.mixins.docker_mixin import DockerMixin
from common.mixins.cloud_mixin import CloudMixin
from common.mixins.bashrc_mixin import BashrcMixin
from common.mixins.version_mixin import VersionMixin

from common.dataclasses_models.image import Image

load_dotenv()

def pre_set_up_cloud_env_hook(func):
    """Decorator to run a pre-set-up-cloud-env step if the subclass/provider defines it."""
    def wrapper(self, *args, **kwargs):
        # Call pre-build step if provider has it
        pre_build = getattr(self.provider, "pre_set_up_cloud_env", None)
        if callable(pre_build):
            print(f"[BaseDeployer] Running pre-set-up-cloud-env step for {self.context}...")
            pre_build(*args, **kwargs)
        return func(self, *args, **kwargs)
    return wrapper

class BaseDeployer(ABC, PackageManagerMixin, DockerMixin, BashrcMixin, VersionMixin):
    PATH_PROJECT_ROOT = "../.."
    PATH_PROJECT_DOCKER = "../Docker"
    ENV = None

    def __init__(self, provider_name, env):
        self.ENV = env
        if self.is_cloud():
            self.cloud_mixin_instance = CloudMixin(
                provider_name=provider_name,
                context=self.CONTEXT,
                env=env
            )

    def deploy(self):
        print(f"=== Deploying {self.__class__.__name__} ===")
        self.verify_os_env()
        self.bundle_packages()
        self.set_up_cloud_env()
        self.generate_image_name()
        self.build_docker_image()
        self.launch_instance()
        self.clean_up()

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
    
    def set_up_cloud_env(self):
        if self.is_cloud():
            print(f"[BaseDeployer] Setting Up Cloud Provider env for {self.CONTEXT}")
            self.cloud_mixin_instance.set_up_provider_env()
        else:
            print(f"[BaseDeployer] Local Deploy: Skipping Cloud env setup for {self.CONTEXT}")
        
        return


    def generate_image_name(self):
        if self.is_cloud():
            print(f"[BaseDeployer] Generating Latest Image Tag from Cloud {self.CONTEXT}")
            images_archives = self.cloud_mixin_instance.get_images_archives()
            self.cloud_mixin_instance.provider.image.tag = self.generate_timestamped_tag(images_archives)
        else:
            print(f"[BaseDeployer] Generating Latest Image Tag from Local {self.CONTEXT}")
            repository = f"{self.CONTEXT}-engine"
            self.image = Image(registry='local', repository=repository, tag="1.0.0")
            images_archives = self.get_images_archives()
            self.image.tag = self.generate_timestamped_tag(images_archives)
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
                image_name=self.image.full_name,
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
                image_name=self.image.full_name,
                port=port,
            )
    
    @abstractmethod
    def clean_up(self):
        pass