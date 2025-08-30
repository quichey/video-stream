import datetime
import os
import sys
from azure.storage.blob import (
    BlobServiceClient,
    generate_blob_sas, BlobSasPermissions
)

from util.env import load_providers_env

load_providers_env()


class LocalStorage():
    RESOURCE_GROUP = os.environ.get("RESOURCE_GROUP_CENTRAL", 'blah')
    ACR_NAME = os.environ.get("CONTAINER_REGISTRY_NAME", 'blah')

    TENANT_ID = os.environ.get("TENANT_ID", 'blah')
    CLIENT_ID = os.environ.get("CLIENT_ID", 'blah')
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET_VALUE", 'blah')

    ACCOUNT_KEY = os.environ.get("STORAGE_ACCOUNT_ACCESS_KEY_1", 'blah')
    ACCOUNT_KEY_CONN = os.environ.get("STORAGE_ACCOUNT_ACCESS_KEY_1_CONN", 'blah')

    STORAGE_ACCOUNT_NAME = os.environ.get("STORAGE_ACCOUNT_NAME")         # env var in practice
    CONTAINER_VIDEOS = "videos"                      # e.g. "videos"
    CONTAINER_IMAGES= "images"

    def __init__(self, cloud_provider="azure"):
        self._blob_service_client = BlobServiceClient.from_connection_string(
            self.ACCOUNT_KEY_CONN
        )

    def get_video_url(self, file_dir, file_name):
        return self.get_media_url(self.CONTAINER_VIDEOS, file_dir=file_dir, file_name=file_name)

    def get_image_url(self, file_dir, file_name):
        return self.get_media_url(self.CONTAINER_IMAGES, file_dir=file_dir, file_name=file_name)

    def get_media_url(self, container, file_dir, file_name):
        # You’ll resolve video_id -> (file_dir, file_name) from your DB

        blob_name = f"{file_dir}/{file_name}"

        bsc = self._blob_service_client

        # Get a user delegation key (AAD-based SAS; safer than account SAS)
        # short lived (e.g., 1 hour)
        now = datetime.datetime.now(datetime.timezone.utc)
        #start = now
        #print(f"\n\n start: {start}")
        #expiry = now + datetime.timedelta(hours=1)
        #print(f"\n\n expiry: {expiry}")
        #key = bsc.get_user_delegation_key(start, expiry)
        #print(f"\n\n after bsc.get_user_delegation_key")

        sas_token = generate_blob_sas(
            account_name=self.STORAGE_ACCOUNT_NAME,
            container_name=container,
            blob_name=blob_name,
            account_key=self.ACCOUNT_KEY,
            permission=BlobSasPermissions(read=True),  # READ only
            expiry=now + datetime.timedelta(minutes=60*2),  # very short-lived
            start=now - datetime.timedelta(minutes=1)     # clock skew
        )

        url = f"https://{self.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{container}/{blob_name}?{sas_token}"
        return url
