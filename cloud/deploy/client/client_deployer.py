from common.base import BaseDeployer

class ClientDeployer(BaseDeployer):
    CONTEXT = "client"
    PACKAGE_MANAGER = "npm"
    PACKAGE_PATH = f"{BaseDeployer.PATH_PROJECT_ROOT}/{CONTEXT}"
    DOCKERFILE = f"{BaseDeployer.PATH_PROJECT_DOCKER}/{CONTEXT}/{CONTEXT}.Dockerfile"
