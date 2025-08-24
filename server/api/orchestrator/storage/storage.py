import datetime
import os
import sys
from azure.identity import DefaultAzureCredential
from azure.storage.blob import (
    BlobServiceClient,
    generate_blob_sas, BlobSasPermissions
)

from util.env import load_providers_env
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../cloud")))
from providers.azure.azure_cli import AzureCLIHelper

load_providers_env()


class Storage():
    RESOURCE_GROUP = os.environ.get("RESOURCE_GROUP_CENTRAL", 'blah')
    ACR_NAME = os.environ.get("CONTAINER_REGISTRY_NAME", 'blah')

    STORAGE_ACCOUNT_NAME = os.environ.get("STORAGE_ACCOUNT_NAME")         # env var in practice
    CONTAINER_VIDEOS = "videos"                      # e.g. "videos"
    CONTAINER_IMAGES= "images"

    def __init__(self):
        self.cli_helper = AzureCLIHelper(resource_group=self.RESOURCE_GROUP, acr_name=self.ACR_NAME)
        self.cli_helper.login()

    def _blob_service_client(self):
        # Works with Managed Identity on Azure; falls back to dev creds locally
        cred = DefaultAzureCredential()
        return BlobServiceClient(
            f"https://{self.STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=cred
        )

    def get_video_url(self, file_dir, file_name):
        return self.get_media_url(self.CONTAINER_VIDEOS, file_dir=file_dir, file_name=file_name)

    def get_image_url(self, file_dir, file_name):
        return self.get_media_url(self.CONTAINER_IMAGES, file_dir=file_dir, file_name=file_name)

    def get_media_url(self, container, file_dir, file_name):
        # You’ll resolve video_id -> (file_dir, file_name) from your DB

        blob_name = f"{file_dir}/{file_name}"

        bsc = self._blob_service_client()

        # Get a user delegation key (AAD-based SAS; safer than account SAS)
        # short lived (e.g., 1 hour)
        now = datetime.datetime.utcnow()
        key = bsc.get_user_delegation_key(now, now + datetime.timedelta(hours=1))

        sas_token = generate_blob_sas(
            account_name=self.STORAGE_ACCOUNT_NAME,
            container_name=container,
            blob_name=blob_name,
            user_delegation_key=key,
            permission=BlobSasPermissions(read=True),  # READ only
            expiry=now + datetime.timedelta(minutes=10),  # very short-lived
            start=now - datetime.timedelta(minutes=1)     # clock skew
        )

        url = f"https://{self.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{container}/{blob_name}?{sas_token}"
        return url
