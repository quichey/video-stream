import datetime
import os
from typing import NewType, Literal
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

from util.env import load_providers_env
from api.orchestrator.storage.base_storage import BaseStorage

# We still call this here for production, but properties will handle the late-binding for tests
load_providers_env()
URL = NewType("URL", str)


class Storage(BaseStorage):
    def __init__(self):
        # We use internal variables to cache the clients once they are built
        self._blob_service_client = None
        self._containter_client = None

    # ---------------------------------------------------------
    # 1. LATE-BINDING CONFIGURATION PROPERTIES
    # These look up os.environ ONLY when called, making them test-friendly.
    # ---------------------------------------------------------
    @property
    def RESOURCE_GROUP(self):
        return os.environ.get("RESOURCE_GROUP_CENTRAL", "blah")

    @property
    def ACR_NAME(self):
        return os.environ.get("CONTAINER_REGISTRY_NAME", "blah")

    @property
    def TENANT_ID(self):
        return os.environ.get("TENANT_ID", "blah")

    @property
    def CLIENT_ID(self):
        return os.environ.get("CLIENT_ID", "blah")

    @property
    def CLIENT_SECRET(self):
        return os.environ.get("CLIENT_SECRET_VALUE", "blah")

    @property
    def ACCOUNT_KEY(self):
        return os.environ.get("STORAGE_ACCOUNT_ACCESS_KEY_1", "blah")

    @property
    def ACCOUNT_KEY_CONN(self):
        return os.environ.get("STORAGE_ACCOUNT_ACCESS_KEY_1_CONN", "blah")

    @property
    def STORAGE_ACCOUNT_NAME(self):
        return os.environ.get("STORAGE_ACCOUNT_NAME")

    @property
    def BLOB_CONTAINER(self):
        return os.environ.get("DEPLOYMENT_ENV")

    # Fixed constants (non-environment dependent)
    DIR_VIDEOS = "videos"
    DIR_IMAGES = "images"

    # ---------------------------------------------------------
    # 2. AZURE CLIENT MANAGEMENT
    # ---------------------------------------------------------
    @property
    def blob_service_client(self):
        if self._blob_service_client is None:
            # Check for "blah" or None to provide a cleaner error message
            conn_str = self.ACCOUNT_KEY_CONN
            if not conn_str or conn_str == "blah":
                raise ValueError(
                    f"Storage Error: ACCOUNT_KEY_CONN is '{conn_str}'. Check your .env or patches."
                )

            self._blob_service_client = BlobServiceClient.from_connection_string(
                conn_str
            )
        return self._blob_service_client

    @property
    def containter_client(self):
        if self._containter_client is None:
            container = self.BLOB_CONTAINER
            if not container:
                raise ValueError(
                    "Storage Error: BLOB_CONTAINER is None. Deployment environment not set."
                )

            self._containter_client = self.blob_service_client.get_container_client(
                container
            )
        return self._containter_client

    # ---------------------------------------------------------
    # 3. CORE STORAGE METHODS
    # ---------------------------------------------------------
    def store_video(self, file_dir, file_name, byte_stream) -> URL | Literal[False]:
        success = self.store_file(file_dir, file_name, byte_stream, self.DIR_VIDEOS)
        return self.get_video_url(file_dir, file_name) if success else False

    def store_image(self, file_dir, file_name, byte_stream) -> URL | Literal[False]:
        success = self.store_file(file_dir, file_name, byte_stream, self.DIR_IMAGES)
        return self.get_image_url(file_dir, file_name) if success else False

    def store_file(self, file_dir, file_name, byte_stream, root_dir) -> bool:
        blob_name = f"{root_dir}/{file_dir}/{file_name}"
        try:
            self.containter_client.upload_blob(
                name=blob_name, data=byte_stream, overwrite=True
            )
            return True
        except Exception as e:
            print(f"\n[STORAGE ERROR] Failed to upload {blob_name}: {e}")
            return False

    # ---------------------------------------------------------
    # 4. URL GENERATION (SAS TOKENS)
    # ---------------------------------------------------------
    def get_video_url(self, file_dir, file_name) -> URL:
        return self.get_media_url(
            self.DIR_VIDEOS, file_dir=file_dir, file_name=file_name
        )

    def get_image_url(self, file_dir, file_name) -> URL:
        return self.get_media_url(
            self.DIR_IMAGES, file_dir=file_dir, file_name=file_name
        )

    def get_media_url(self, root_dir, file_dir, file_name) -> URL:
        blob_name = f"{root_dir}/{file_dir}/{file_name}"
        now = datetime.datetime.now(datetime.timezone.utc)

        # These property calls now correctly retrieve patched values during tests
        account_name = self.STORAGE_ACCOUNT_NAME
        container = self.BLOB_CONTAINER
        account_key = self.ACCOUNT_KEY

        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=container,
            blob_name=blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=now + datetime.timedelta(minutes=120),
            start=now - datetime.timedelta(minutes=1),  # Handling clock skew
        )

        return f"https://{account_name}.blob.core.windows.net/{container}/{blob_name}?{sas_token}"
