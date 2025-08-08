from dotenv import load_dotenv
import os

from azure import azure_cli

load_dotenv(dotenv_path="./azure/.env")

azure_cli_helper = azure_cli.AzureCLIHelper(
    resource_group=os.environ.get("RESOUCE_GROUP_CENTRAL", 'blah'),
    acr_name=os.environ.get("CONTAINER_REGISTRY_NAME", 'blah'),
)