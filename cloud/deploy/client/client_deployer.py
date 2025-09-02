from common.base import BaseDeployer
from util.file_handling import update_file

class ClientDeployer(BaseDeployer):
    CONTEXT = "client"
    PACKAGE_MANAGER = "npm"
    PACKAGE_PATH = f"{BaseDeployer.PATH_PROJECT_ROOT}/{CONTEXT}"
    DOCKERFILE = f"{BaseDeployer.PATH_PROJECT_DOCKER}/{CONTEXT}/{CONTEXT}.Dockerfile"



    def pre_set_up_cloud_env(self):
        provider = self.cloud_mixin_instance.provider
        client_container_url = provider.get_container_url()
        #TODO: replace client_container_url <client> with <server>?
        server_container_url = client_container_url.replace(self.CONTEXT, "server")
        #deployment_env = self.ENV
        #TODO: write to cloud/providers/azure/.env
        # REACT_APP_SERVER_URL={server_container_url}
        dot_env_file_path = "../providers/azure/.env"
        update_file(dot_env_file_path, "REACT_APP_SERVER_APP_URL=", f"REACT_APP_SERVER_APP_URL={server_container_url}")

        #TODO: update client/package.json? home: attribute
        package_dot_json_path = "../../client/package.json"
        #TODO: think about git history with package.json homepage attribute changing
        update_file(package_dot_json_path, '"homepage":', f'"homepage": {client_container_url}')
