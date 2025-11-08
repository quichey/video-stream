from abc import ABC, abstractmethod
from typing_extensions import override
from dotenv import load_dotenv
import shutil
import os

from common.mixins.cloud_mixin.cloud_container_mixin import CloudContainerMixin
from common.base import BaseDeployer
from common.dataclasses_models.image import Image

load_dotenv()


# TODO: db deploy
class BaseContainerDeployer(BaseDeployer, ABC):
    CLOUD_MIXIN_CLASS = CloudContainerMixin

    @override
    def is_first_deploy(self) -> bool:
        # TODO: need to locate the old code i had for doing first deployment
        # vs subsequent

        # why did do these changes before?
        # was deploying new testing infra
        # i think testing out the scripts to automatically start/stop containers
        # then realized Azure Container Apps cannot do that
        # then tried switching to Azure Container Instances
        # but not certain exactly what necessitated different deploy procedures
        # based off of first deployment or not
        # i believe it is generate image name
        # The versioning would not have image yet on first deployment
        # So for fist deployment, need to use different logic for determinging
        # full version tag
        if self.is_cloud():
            print(
                f"[BaseDeployer] Generating Latest Image Tag from Cloud {self.CONTEXT}"
            )
            try:
                images_archives = self.cloud_mixin_instance.get_images_archives()
                if images_archives == []:
                    return True
                return False
            except Exception:
                return True
        else:
            print(
                f"[BaseDeployer] Generating Latest Image Tag from Local {self.CONTEXT}"
            )
            repository = f"{self.CONTEXT}-engine"
            self.image = Image(registry="local", repository=repository, tag="1.0.0")
            images_archives = self.get_images_archives()
            self.image.tag = self.generate_timestamped_tag(images_archives)
        return

    @override
    def do_first_deploy(self):
        print(f"=== Deploying {self.__class__.__name__} ===")
        self.verify_os_env()
        self.bundle_packages()
        self.set_up_cloud_env()
        self.generate_first_image_name()
        self.build_docker_image()
        self.launch_instance()
        self.clean_up()

    @override
    def do_update(self):
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
                    raise EnvironmentError(
                        f"{tool} not found. Run deploy/os/linux/env_setup.sh first."
                    )
        elif self.PACKAGE_MANAGER == "poetry":
            if shutil.which("poetry") is None:
                raise EnvironmentError(
                    "poetry not found. Run deploy/os/linux/env_setup.sh first."
                )
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

    def generate_first_image_name(self):
        pass

    def generate_image_name(self):
        if self.is_cloud():
            print(
                f"[BaseDeployer] Generating Latest Image Tag from Cloud {self.CONTEXT}"
            )
            images_archives = self.cloud_mixin_instance.get_images_archives()
            self.cloud_mixin_instance.provider.image.tag = (
                self.generate_timestamped_tag(images_archives)
            )
        else:
            print(
                f"[BaseDeployer] Generating Latest Image Tag from Local {self.CONTEXT}"
            )
            repository = f"{self.CONTEXT}-engine"
            self.image = Image(registry="local", repository=repository, tag="1.0.0")
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
            port = os.environ.get(f"PORT_{machine_context}", "local")
            self.docker_run(
                image_name=self.image.full_name,
                port=port,
            )

    @abstractmethod
    def clean_up(self):
        pass
