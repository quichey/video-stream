from .aws_provider import AWSProvider
from .azure_provider import AzureProvider
from .gcp_provider import GoogleCloudProvider

def get_provider_class(provider_name):
    providers = {
        "aws": AWSProvider,
        "azure": AzureProvider,
        "gcp": GoogleCloudProvider,
    }
    return providers[provider_name.lower()]
