from cloud_providers_deployment import get_provider_class


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
    def __init__(self, provider_name, context, env):
        self.context = context
        self.provider = get_provider_class(provider_name)(context, env)

    def set_up_provider_env(self):
        self.provider.set_up_env()
        return
