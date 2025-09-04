import datetime
import os
from typing import NewType, Literal
from azure.storage.blob import (
    BlobServiceClient,
    generate_blob_sas, BlobSasPermissions
)

from util.env import load_providers_env
from api.orchestrator.storage.base_storage import BaseStorage

load_providers_env()
URL = NewType("URL", str)

class Storage(BaseStorage):
    RESOURCE_GROUP = os.environ.get("RESOURCE_GROUP_CENTRAL", 'blah')
    ACR_NAME = os.environ.get("CONTAINER_REGISTRY_NAME", 'blah')

    TENANT_ID = os.environ.get("TENANT_ID", 'blah')
    CLIENT_ID = os.environ.get("CLIENT_ID", 'blah')
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET_VALUE", 'blah')

    ACCOUNT_KEY = os.environ.get("STORAGE_ACCOUNT_ACCESS_KEY_1", 'blah')
    ACCOUNT_KEY_CONN = os.environ.get("STORAGE_ACCOUNT_ACCESS_KEY_1_CONN", 'blah')

    STORAGE_ACCOUNT_NAME = os.environ.get("STORAGE_ACCOUNT_NAME")         # env var in practice
    DIR_VIDEOS = "videos"                      # e.g. "videos"
    DIR_IMAGES = "images"
    BLOB_CONTAINER = os.environ.get("BLOB_CONTAINER")  

    def __init__(self, cloud_provider="azure"):
        self._blob_service_client = BlobServiceClient.from_connection_string(
            self.ACCOUNT_KEY_CONN
        )
        self._containter_client = self._blob_service_client.get_container_client(
            self.BLOB_CONTAINER
        )

    def store_video(self, file_dir, file_name, byte_stream) -> URL | Literal[False]:
        success = self.store_file(file_dir, file_name, byte_stream, self.DIR_VIDEOS)
        if success:
            return self.get_video_url(file_dir, file_name)
        else:
            return False

    def store_image(self, file_dir, file_name, byte_stream) -> URL | Literal[False]:
        success = self.store_file(file_dir, file_name, byte_stream, self.DIR_IMAGES)
        if success:
            return self.get_image_url(file_dir, file_name)
        else:
            return False

    def store_file(self, file_dir, file_name, byte_stream, root_dir) -> bool:
        container_client = self._containter_client
        blob_name = f"{root_dir}/{file_dir}/{file_name}"
        try:
            container_client.upload_blob(name=blob_name, data=byte_stream, overwrite=True)
            return True
        except Exception as e:
            print(f"\n\n Exception: {e} ")
            return False

    def get_video_url(self, file_dir, file_name) -> URL:
        return self.get_media_url(self.DIR_VIDEOS, file_dir=file_dir, file_name=file_name)

    def get_image_url(self, file_dir, file_name) -> URL:
        return self.get_media_url(self.DIR_IMAGES, file_dir=file_dir, file_name=file_name)

    def get_media_url(self, root_dir, file_dir, file_name) -> URL:
        # You’ll resolve video_id -> (file_dir, file_name) from your DB

        blob_name = f"{root_dir}/{file_dir}/{file_name}"


        # Get a user delegation key (AAD-based SAS; safer than account SAS)
        # short lived (e.g., 1 hour)
        now = datetime.datetime.now(datetime.timezone.utc)
        #start = now
        #print(f"\n\n start: {start}")
        #expiry = now + datetime.timedelta(hours=1)
        #print(f"\n\n expiry: {expiry}")
        #key = bsc.get_user_delegation_key(start, expiry)
        #print(f"\n\n after bsc.get_user_delegation_key")

        container = self.BLOB_CONTAINER
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
