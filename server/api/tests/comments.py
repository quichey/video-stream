import pytest
from datetime import datetime
from flask import json
from unittest.mock import patch

from api import create_app
from api.orchestrator.session.state.comments import (
    COMMENTS_FIRST_PAGE_SIZE,
    COMMENTS_NEXT_PAGE_SIZE,
)

# --- GLOBAL TEST FIXTURES ---


@pytest.fixture(autouse=True, scope="session")
def force_cors_origins():
    """Forces flask_cors to have a list to iterate over, preventing NoneType crashes."""
    with patch("flask_cors.core.get_cors_origins", return_value=["*"]):
        yield


@pytest.fixture()
def mock_db_results():
    """
    Dynamically mocks SQLAlchemy results based on which table is being queried.
    """
    # Database for Videos (3 columns: file_name, file_dir, user_name)
    video_db = [("test_video.mp4", "/videos/test/", "KyleNgo")]

    # Database for Comments (2 columns: comment, user_name)
    comment_db = [(f"Comment {i}", f"User {i}") for i in range(100)]

    with patch(
        "api.orchestrator.session.state.state_module.StateModule.engine"
    ) as mock_engine:
        mock_conn = mock_engine.connect.return_value.__enter__.return_value

        def dynamic_execute(stmt):
            # 1. Identify which table we are hitting by looking at the statement string
            stmt_str = str(stmt).lower()

            # 2. Handle Video queries (looking for 'file_name' or 'videos' table)
            if "file_name" in stmt_str or "videos" in stmt_str:
                return video_db

            # 3. Handle Comment queries with Pagination
            limit = (
                stmt._limit_clause.value
                if hasattr(stmt, "_limit_clause") and stmt._limit_clause is not None
                else 100
            )
            offset = (
                stmt._offset_clause.value
                if hasattr(stmt, "_offset_clause") and stmt._offset_clause is not None
                else 0
            )

            return comment_db[offset : offset + limit]

        mock_conn.execute.side_effect = dynamic_execute
        yield mock_conn


@pytest.fixture()
def mock_storage():
    """Mocks the Azure storage call to return a dummy URL."""
    with patch(
        "api.orchestrator.session.state.watch_video.STORAGE"
    ) as mock_storage_obj:
        mock_storage_obj.get_video_url.return_value = "http://localhost/test_video.mp4"
        yield mock_storage_obj


@pytest.fixture()
def app_info(mock_db_results, mock_storage):
    """Initializes the Flask app with the dynamic DB mock."""
    app = create_app()
    app.config.update({"TESTING": True})

    # Mock the video info extraction to return a valid ID
    with patch(
        "api.orchestrator.session.state.watch_video.extract_video_info"
    ) as mock_info:
        mock_info.return_value = {"id": 1}
        yield {"client": app.test_client(), "test_user": 0}


# --- HELPER FUNCTIONS ---


def extract_token(response):
    """Extracts session info or token from the response JSON."""
    data = response.get_json()
    return data.get("session_info") or data.get("session_token")


def package_session_info(user):
    return {"user_id": 0, "user_name": user}


def get_first_page(client, user):
    # 1. Initialize the video state
    video_payload = package_session_info(user)
    video_payload["video_id"] = 1
    client.post(
        "/video", data=json.dumps(video_payload), content_type="application/json"
    )

    # 2. Fetch the first page of comments
    response = client.post(
        "/getcomments",
        data=json.dumps(package_session_info(user)),
        content_type="application/json",
    )

    data = response.get_json().get("comment_data", [])
    num_comments = len(data)

    # ASSERTION: Verify the first page respects the limit
    assert num_comments <= COMMENTS_FIRST_PAGE_SIZE
    print(f"\n[Setup] First page received: {num_comments} comments.")

    return extract_token(response)


# --- TESTS ---


def test_infinite_scroll(app_info):
    client = app_info["client"]
    test_user = app_info["test_user"]

    # Mock sleep so the 10-minute check in logic is bypassed
    with patch("time.sleep", return_value=None):
        token = get_first_page(client, test_user)
        assert token is not None, "Failed to retrieve session token."

        # Test subsequent pages
        for i in range(3):
            request_data = package_session_info(test_user)
            request_data["token"] = token

            start_time = datetime.now()
            response = client.post(
                "/getcomments",
                data=json.dumps(request_data),
                content_type="application/json",
            )
            ms_delta = (datetime.now() - start_time).total_seconds() * 1000

            data = response.get_json().get("comment_data", [])

            # PAGINATION ASSERTION: Verify subsequent pages respect the smaller limit
            assert len(data) <= COMMENTS_NEXT_PAGE_SIZE
            assert ms_delta < 200, f"Latency too high: {ms_delta}ms"

            # Refresh token if rotated
            token = extract_token(response) or token

            print(
                f"Verified page {i + 1}: Received {len(data)} comments in {ms_delta:.2f}ms"
            )
