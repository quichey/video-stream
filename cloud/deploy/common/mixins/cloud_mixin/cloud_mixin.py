class CloudMixin:
    GET_PROVIDER_CLASS_FUNC = None

    def __init__(self, provider_name, context, env, *args, **kwargs):
        self.context = context
        self._provider = self.GET_PROVIDER_CLASS_FUNC(provider_name, *args, **kwargs)(
            context, env
        )

    def set_up_provider_env(self):
        self.provider.set_up_env()
        return

    @property
    def provider(self):
        return self._provider
