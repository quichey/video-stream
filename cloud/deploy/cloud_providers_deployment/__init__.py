from .aws.aws_provider import AWSProvider
from .azure.azure_container_provider import AzureContainerProvider
from .azure.azure_db_provider import AzureDBCloudProvider
from .gcp.gcp_container_provider import GoogleCloudContainerProvider


def get_provider_class_container(provider_name):
    providers = {
        "aws": AWSProvider,
        "azure": AzureContainerProvider,
        "gcp": GoogleCloudContainerProvider,
    }
    return providers[provider_name.lower()]


def get_provider_class_db(provider_name):
    providers = {
        "aws": AWSProvider,
        "azure": AzureDBCloudProvider,
        # "gcp": GoogleCloudDBProvider,
    }
    return providers[provider_name.lower()]
