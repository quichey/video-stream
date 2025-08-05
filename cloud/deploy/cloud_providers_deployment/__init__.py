from .aws_provider import AWSProvider
from .azure_provider import AzureProvider
from .gcp_provider import GCPProvider

def get_provider_class(provider_name):
    providers = {
        "aws": AWSProvider,
        "azure": AzureProvider,
        "gcp": GCPProvider,
    }
    return providers[provider_name.lower()]
