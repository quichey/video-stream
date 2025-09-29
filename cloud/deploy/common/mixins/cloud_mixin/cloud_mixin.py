def pre_build_hook(func):
    """Decorator to run a pre-build step if the subclass/provider defines it."""

    def wrapper(self, *args, **kwargs):
        # Call pre-build step if provider has it
        pre_build = getattr(self.provider, "pre_build_image_cloud", None)
        if callable(pre_build):
            print(f"[CloudMixin] Running pre-build step for {self.context}...")
            pre_build(*args, **kwargs)
        return func(self, *args, **kwargs)

    return wrapper


class CloudMixin:
    GET_PROVIDER_CLASS_FUNC = None

    def __init__(self, provider_name, context, env):
        self.context = context
        self._provider = self.GET_PROVIDER_CLASS_FUNC(provider_name)(context, env)

    def set_up_provider_env(self):
        self.provider.set_up_env()
        return

    @property
    def provider(self):
        return self._provider
