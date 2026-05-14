from unittest.mock import patch


def test_watch_video_id_folder_matching(client, load_state):
    """
    Verifies that the /video route correctly handles the 'user_id as file_dir'
    convention established in the production logic.
    """
    # 1. Seed the DB with matching ID and Directory
    load_state("video_watch_state")

    with patch("api.orchestrator.session.state.watch_video.STORAGE") as mock_storage:
        # 2. Mock storage to return a URL based on the user-id directory
        mock_storage.get_video_url.return_value = (
            "https://mockstorage.com/10/test_video.mp4"
        )

        # 3. Request video ID 500
        payload = {"video_id": 500}
        response = client.post("/video", json=payload)

        # 4. Assertions
        assert response.status_code == 200
        data = response.get_json()
        video_data = data["video_data"]

        # Verify the 'user_id as folder' logic
        assert video_data["user_name"] == "content_creator"
        assert video_data["file_dir"] == "10"
        assert video_data["file_name"] == "test_video.mp4"

        # Verify Storage was called with the user_id (10) as the first argument
        mock_storage.get_video_url.assert_called_once_with("10", "test_video.mp4")
