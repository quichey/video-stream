import pytest
from unittest.mock import MagicMock, patch
from api.orchestrator.session.SessionManagement import SessionManagement


@pytest.fixture
def manager():
    return SessionManagement()


def test_needs_new_session_logic(manager):
    """Verifies the logic that triggers a completely new session."""
    # Block 1: No cookie, no user info -> Should be True
    with (
        patch(
            "api.orchestrator.session.SessionManagement.extract_long_term_cookie",
            return_value=None,
        ),
        patch(
            "api.orchestrator.session.SessionManagement.has_user_info",
            return_value=False,
        ),
    ):
        assert manager.needs_new_session(MagicMock()) is True

    # Block 2: Cookie exists -> Should be False
    with (
        patch(
            "api.orchestrator.session.SessionManagement.extract_long_term_cookie",
            return_value="existing-id",
        ),
        patch(
            "api.orchestrator.session.SessionManagement.has_user_info",
            return_value=False,
        ),
    ):  # Added this mock
        # If a cookie exists, we don't need a *new* session
        assert manager.needs_new_session(MagicMock()) is False


def test_needs_restore_lost_session(manager):
    """Tests identifying when a user has a cookie but the server lost the state (e.g. server restart)."""
    cookie_id = "stale-id"

    with patch(
        "api.orchestrator.session.SessionManagement.extract_long_term_cookie",
        return_value=cookie_id,
    ):
        # Registry is empty, so this ID is 'lost'
        assert manager.needs_restore_lost_session(MagicMock()) is True

        # Add it to registry
        mock_session = MagicMock()
        manager.SESSION_REGISTRY.sessions[cookie_id] = mock_session

        # Now it's no longer lost
        assert manager.needs_restore_lost_session(MagicMock()) is False


def test_session_token_hack_search(manager):
    """Tests the logic that finds a browser session based on a tab token."""
    # 1. Setup a fake browser session with a nested tab session token
    target_token = "find-me"

    mock_tab = MagicMock()
    mock_tab.token = target_token

    mock_browser = MagicMock()
    mock_browser.anonymous_tab_session = mock_tab
    mock_browser.LONG_TERM_COOKIE_ID = "browser-123"

    # 2. Add to manager
    manager.SESSION_REGISTRY.sessions["browser-123"] = mock_browser

    # 3. Test the search (HACK) logic
    # We want to see if it correctly finds 'mock_browser' when we provide 'find-me'
    response = MagicMock()

    with patch.object(mock_browser, "on_request") as mock_on_request:
        manager.on_request(MagicMock(), response, SESSION_TOKEN_HACK=target_token)

        # Verify it found the right browser session and called its on_request
        mock_on_request.assert_called_once()


def test_add_browser_session(manager):
    """Ensures sessions are correctly added to the internal registry."""
    with patch(
        "api.orchestrator.session.SessionManagement.BrowserSession"
    ) as MockBrowser:
        # Setup mock browser instance
        instance = MockBrowser.return_value
        instance.LONG_TERM_COOKIE_ID = "new-cookie-id"

        manager.add_browser_session(MagicMock(), MagicMock())

        assert "new-cookie-id" in manager.SESSION_REGISTRY.sessions
        assert manager.SESSION_REGISTRY.sessions["new-cookie-id"] == instance
