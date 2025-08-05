class BaseCloudProvider:
    def deploy_app(self, *args, **kwargs):
        raise NotImplementedError

    def destroy(self, *args, **kwargs):
        raise NotImplementedError
