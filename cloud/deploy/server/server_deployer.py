from typing_extensions import override

from common.base import BaseDeployer
from util.file_handling import update_file

class ServerDeployer(BaseDeployer):
    CONTEXT = "server"
    PACKAGE_MANAGER = "poetry"
    PACKAGE_PATH = f"{BaseDeployer.PATH_PROJECT_ROOT}/{CONTEXT}"
    DOCKERFILE = f"{BaseDeployer.PATH_PROJECT_DOCKER}/{CONTEXT}/{CONTEXT}.Dockerfile"

    def pre_set_up_cloud_env(self):
        provider = self.cloud_mixin_instance.provider
        server_container_url = provider.get_container_url().stdout.strip("\n")
        server_container_url = f"https://{server_container_url}"
        print(f"\n\n server_container_url: {server_container_url} \n\n")
        #TODO: replace client_container_url <client> with <server>?
        client_container_url = server_container_url.replace(self.CONTEXT, "client")
        print(f"\n\n client_container_url: {client_container_url} \n\n")
        #deployment_env = self.ENV
        #TODO: write to cloud/providers/azure/.env
        # REACT_APP_SERVER_URL={server_container_url}
        dot_env_file_path = "../providers/azure/.env"
        update_file(dot_env_file_path, "CLIENT_APP_URL=", f"CLIENT_APP_URL={client_container_url}\n")

    @override
    def clean_up(self):
        return