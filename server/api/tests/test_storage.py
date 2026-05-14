import io
from unittest.mock import patch
from api.orchestrator.storage import Storage

# ---------------------------------------------------------
# UNIT TESTS FOR STORAGE CLASS
# ---------------------------------------------------------


def test_store_video_and_get_valid_url(test_blob_storage):
    """
    HIL Test: Verifies that a video can be uploaded to the real
    Azure 'test' container and returns a valid SAS-authenticated URL.
    """
    upload_video, _ = test_blob_storage

    # Simulate a video file in memory
    fake_video_content = b"fake-mp4-binary-data-kyle-dev"
    video_stream = io.BytesIO(fake_video_content)
    file_name = "interview_demo_video.mp4"
    file_dir = "user_123"

    # Action
    url = upload_video(file_dir, file_name, video_stream)

    # Assertions
    assert url is not False, "Upload failed; check Azure connectivity."
    assert "https://" in url
    assert "test" in url, "Safety Failure: Did not upload to the 'test' container!"
    assert "sig=" in url, "Security Failure: SAS token was not generated."


def test_store_image_places_in_correct_directory(test_blob_storage):
    """
    Hierarchy Test: Verifies that the Storage class respects the
    virtual directory structure for images vs videos.
    """
    _, upload_image = test_blob_storage

    fake_image = io.BytesIO(b"fake-png-data")
    file_name = "profile_icon.png"
    file_dir = "kyle_ngo"

    # Action
    url = upload_image(file_dir, file_name, fake_image)

    # Verify the URL structure contains the 'images' root dir instead of 'videos'
    assert "/images/" in url
    assert "profile_icon.png" in url


def test_store_file_failure_handling():
    """
    Robustness Test: Mocks a network failure to ensure the
    application logic handles exceptions gracefully without crashing.
    """
    storage = Storage()
    fake_data = io.BytesIO(b"critical-data")

    # We surgically mock the upload_blob method to raise an exception
    # This simulates a 'Radio Link Failure' or 'Azure Outage'
    with patch("azure.storage.blob.ContainerClient.upload_blob") as mock_upload:
        mock_upload.side_effect = Exception("Simulated Network Timeout")

        # Action
        result = storage.store_file("error_dir", "fail.txt", fake_data, "root")

        # Assertions
        assert result is False, "Storage class should return False on exception."


def test_sas_token_clock_skew_logic():
    """
    Logic Test: Verifies that the SAS token includes the start (st)
    and expiry (se) parameters, supporting the 1-minute look-back logic.
    """
    storage = Storage()
    url = storage.get_video_url("test_dir", "test_file.mp4")

    # 'st' is the start time, 'se' is expiry. Both are vital for access control.
    assert "st=" in url
    assert "se=" in url
