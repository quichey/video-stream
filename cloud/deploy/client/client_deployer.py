from common.base import BaseDeployer
from util.file_handling import update_file

from util.subprocess_helper import run_cmd_with_retries

class ClientDeployer(BaseDeployer):
    CONTEXT = "client"
    PACKAGE_MANAGER = "npm"
    PACKAGE_PATH = f"{BaseDeployer.PATH_PROJECT_ROOT}/{CONTEXT}"
    DOCKERFILE = f"{BaseDeployer.PATH_PROJECT_DOCKER}/{CONTEXT}/{CONTEXT}.Dockerfile"
    PACKAGE_JSON_PATH = "../../client/package.json"



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
        package_dot_json_path = self.PACKAGE_JSON_PATH
        cp_cmd = f"cp {package_dot_json_path} {package_dot_json_path}.bk"
        cp_cmd = cp_cmd.split(" ")
        run_cmd_with_retries(cp_cmd)
        #TODO: think about git history with package.json homepage attribute changing
        update_file(package_dot_json_path, '"homepage":', f'"homepage": {client_container_url}')

    def clean_up(self):
        package_dot_json_path = self.PACKAGE_JSON_PATH
        cp_cmd = f"cp {package_dot_json_path}.bk {package_dot_json_path}"
        cp_cmd = cp_cmd.split(" ")
        run_cmd_with_retries(cp_cmd)
        rm_cmd = f"rm {package_dot_json_path}.bk"
        run_cmd_with_retries(rm_cmd)
