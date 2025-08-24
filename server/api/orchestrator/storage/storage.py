import datetime
import os
import sys
from azure.identity import ClientSecretCredential
from azure.storage.blob import (
    BlobServiceClient,
    generate_blob_sas, BlobSasPermissions
)

from util.env import load_providers_env

load_providers_env()


class Storage():
    RESOURCE_GROUP = os.environ.get("RESOURCE_GROUP_CENTRAL", 'blah')
    ACR_NAME = os.environ.get("CONTAINER_REGISTRY_NAME", 'blah')

    TENANT_ID = os.environ.get("TENANT_ID", 'blah')
    CLIENT_ID = os.environ.get("CLIENT_ID", 'blah')
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET_VALUE", 'blah')

    STORAGE_ACCOUNT_NAME = os.environ.get("STORAGE_ACCOUNT_NAME")         # env var in practice
    CONTAINER_VIDEOS = "videos"                      # e.g. "videos"
    CONTAINER_IMAGES= "images"

    def __init__(self, cloud_provider="azure"):
        print(f"\n\n TENANT_ID: {self.TENANT_ID} \n\n")
        print(f"\n\n CLIENT_ID: {self.CLIENT_ID} \n\n")
        self.credential = ClientSecretCredential(
            tenant_id=self.TENANT_ID,
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            #additionally_allowed_tenants=["*"]  # allow any tenant
        )
        self._blob_service_client = BlobServiceClient(
            f"https://{self.STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=self.credential
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
        now = datetime.datetime.utcnow()
        key = bsc.get_user_delegation_key(now, now + datetime.timedelta(hours=1))

        sas_token = generate_blob_sas(
            account_name=self.STORAGE_ACCOUNT_NAME,
            container_name=container,
            blob_name=blob_name,
            user_delegation_key=key,
            permission=BlobSasPermissions(read=True),  # READ only
            expiry=now + datetime.timedelta(minutes=60*2),  # very short-lived
            start=now - datetime.timedelta(minutes=1)     # clock skew
        )

        url = f"https://{self.STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{container}/{blob_name}?{sas_token}"
        return url
