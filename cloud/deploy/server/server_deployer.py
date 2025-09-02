from typing_extensions import override

from common.base import BaseDeployer

class ServerDeployer(BaseDeployer):
    CONTEXT = "server"
    PACKAGE_MANAGER = "poetry"
    PACKAGE_PATH = f"{BaseDeployer.PATH_PROJECT_ROOT}/{CONTEXT}"
    DOCKERFILE = f"{BaseDeployer.PATH_PROJECT_DOCKER}/{CONTEXT}/{CONTEXT}.Dockerfile"

    @override
    def clean_up(self):
        return