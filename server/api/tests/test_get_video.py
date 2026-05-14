from unittest.mock import patch


def test_watch_video_integration(client, load_state):
    """
    Integration test for the /video POST route.
    Verifies that the orchestrator correctly joins video and user data
    and interacts with the storage layer.
    """
    # 1. Load the specific state for this test
    load_state("video_watch_state")

    # 2. Mock the STORAGE object to avoid real Azure/Cloud calls
    # We patch it where it is used in the watch_video logic
    with patch("api.orchestrator.session.state.watch_video.STORAGE") as mock_storage:
        mock_storage.get_video_url.return_value = (
            "https://mockstorage.com/test_folder/test_video.mp4"
        )

        # 3. Define the payload (extract_video_info expects 'id' in the request)
        # Since it's a POST, we send it as JSON
        payload = {"id": 500}

        # 4. Hit the route
        response = client.post("/video", json=payload)

        # 5. Assertions
        assert response.status_code == 200

        data = response.get_json()

        # Verify the database join worked (User ID 10 -> 'content_creator')
        assert data["user_name"] == "content_creator"
        assert data["file_name"] == "test_video.mp4"
        assert data["file_dir"] == "test_folder"

        # Verify storage integration
        assert data["video_url"] == "https://mockstorage.com/test_folder/test_video.mp4"
        mock_storage.get_video_url.assert_called_once_with(
            "test_folder", "test_video.mp4"
        )
