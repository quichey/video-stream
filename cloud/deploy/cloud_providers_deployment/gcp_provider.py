from .base_provider import BaseCloudProvider

class GoogleCloudProvider(BaseCloudProvider):
    def get_build_cmd(self, dockerfile, package_path, tag):
        raise NotImplementedError

    def get_run_cmd(self, image_name, tag):
        raise NotImplementedError

