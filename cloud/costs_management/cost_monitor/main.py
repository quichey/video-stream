# run_monitor.py
from cloud_providers.azure_provider import AzureProvider

if __name__ == "__main__":
    provider = AzureProvider("azure_config_example.yaml")
    provider.run_monitoring()
