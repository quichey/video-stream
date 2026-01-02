from .aws.aws_provider import AWSProvider
from .azure.azure_container_provider import AzureContainerProvider
from .azure.azure_mysql_db import AzureMySQLDBProvider
from .gcp.gcp_container_provider import GoogleCloudContainerProvider


def get_provider_class_container(provider_name, *args, **kwargs):
    providers = {
        "aws": AWSProvider,
        "azure": AzureContainerProvider,
        "gcp": GoogleCloudContainerProvider,
    }
    return providers[provider_name.lower()]


def get_provider_class_db(provider_name, dialect):
    providers = {
        "aws": AWSProvider,
        "azure": {
            "mysql": AzureMySQLDBProvider,
            # "postgres": AzurePostgre,
        },
        # "gcp": GoogleCloudDBProvider,
    }
    return providers[provider_name.lower()][dialect]
