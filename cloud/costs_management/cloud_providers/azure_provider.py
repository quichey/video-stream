from cloud_providers.base_provider import BaseProvider

class AzureProvider(BaseProvider):
    CONTEXT = "server"
    PACKAGE_MANAGER = "poetry"
    PACKAGE_PATH = f"{BaseProvider.PATH_PROJECT_ROOT}/{CONTEXT}"
    IMAGE_NAME = f"{CONTEXT}-engine"
    DOCKERFILE = f"{BaseProvider.PATH_PROJECT_DOCKER}/{CONTEXT}/{CONTEXT}.Dockerfile"
    TAG = f"gcr.io/my-project/{CONTEXT}-engine:1.0.0"
