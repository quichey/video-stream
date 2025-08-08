from dotenv import load_dotenv
import os

from azure import azure_cli

load_dotenv(dotenv_path="./azure/.env")

RESOUCE_GROUP_CENTRAL=os.environ.get("RESOUCE_GROUP_CENTRAL", 'blah')
CONTAINER_REGISTRY_NAME=os.environ.get("CONTAINER_REGISTRY_NAME", 'blah')
MYSQL_DB_NAME=os.environ.get("MYSQL_DB_NAME", 'blah')

azure_cli_helper = azure_cli.AzureCLIHelper(
    resource_group=RESOUCE_GROUP_CENTRAL,
    acr_name=CONTAINER_REGISTRY_NAME,
)

def enable_auto_stop():
    azure_cli_helper.login()
    #azure_cli_helper.acr_login()
    print(f"\n\n MYSQL_DB_NAME: {MYSQL_DB_NAME} \n\n")
    azure_cli_helper.enable_mysql_flexible_auto_stop(
        server_name=MYSQL_DB_NAME, 
        resource_group=RESOUCE_GROUP_CENTRAL,
    )