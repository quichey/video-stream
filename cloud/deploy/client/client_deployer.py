from common.base import BaseDeployer

class ClientDeployer(BaseDeployer):
    CONTEXT = "client"
    PACKAGE_MANAGER = "npm"
    PACKAGE_PATH = f"{BaseDeployer.PATH_PROJECT_ROOT}/{CONTEXT}"
    DOCKERFILE = f"{BaseDeployer.PATH_PROJECT_DOCKER}/{CONTEXT}/{CONTEXT}.Dockerfile"



    def pre_set_up_cloud_env(self):
        provider = self.cloud_mixin_instance.provider
        client_container_url = provider.get_container_url()
        #TODO: replace client_container_url <client> with <server>?
        server_container_url = pass
        deployment_env = self.ENV
        #TODO: write to cloud/providers/azure/.env
        # REACT_APP_SERVER_URL={server_container_url}
