# server/api/storage.py
import datetime
from flask import Blueprint, jsonify, request
from azure.identity import DefaultAzureCredential
from azure.storage.blob import (
    BlobServiceClient,
    generate_blob_sas, BlobSasPermissions
)

bp = Blueprint("media", __name__)

STORAGE_ACCOUNT_NAME = "youracct"         # env var in practice
CONTAINER = "videos"                      # e.g. "videos"

def _blob_service_client():
    # Works with Managed Identity on Azure; falls back to dev creds locally
    cred = DefaultAzureCredential()
    return BlobServiceClient(
        f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
        credential=cred
    )

@bp.route("/media-url", methods=["POST"])
def media_url():
    data = request.get_json(force=True)
    # You’ll resolve video_id -> (file_dir, file_name) from your DB
    video_id = data["video_id"]

    # Example mapping; replace with DB lookup
    file_dir, file_name = "1", "test_video_1.mp4"
    blob_name = f"{file_dir}/{file_name}"

    bsc = _blob_service_client()

    # Get a user delegation key (AAD-based SAS; safer than account SAS)
    # short lived (e.g., 1 hour)
    now = datetime.datetime.utcnow()
    key = bsc.get_user_delegation_key(now, now + datetime.timedelta(hours=1))

    sas_token = generate_blob_sas(
        account_name=STORAGE_ACCOUNT_NAME,
        container_name=CONTAINER,
        blob_name=blob_name,
        user_delegation_key=key,
        permission=BlobSasPermissions(read=True),  # READ only
        expiry=now + datetime.timedelta(minutes=10),  # very short-lived
        start=now - datetime.timedelta(minutes=1)     # clock skew
    )

    url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER}/{blob_name}?{sas_token}"
    return jsonify({"url": url})
