import pytest
from unittest.mock import MagicMock, patch
from api.orchestrator.session.tab_session.TabSession import TabSession
from api.util.error_handling import SecurityError


# 1. Create a concrete subclass for testing
class MockTab(TabSession):
    def key(self):
        return "test_key"


@pytest.fixture
def session():
    req = MagicMock()
    res = MagicMock()
    # Mock extract_session_token to return None initially
    with patch(
        "api.orchestrator.session.tab_session.TabSession.extract_session_token",
        return_value=None,
    ):
        return MockTab(req, res)


def test_determine_event_mapping(session):
    # Test the router
    req = MagicMock()
    req.path = "/video"
    assert session.determine_event(req) == "watch_video"

    req.path = "/video-list"
    assert session.determine_event(req) == "home"


def test_authenticate_session_security_fail(session):
    # Setup: Session has a token
    session.TOKEN = "valid-token"

    # Mock request with a DIFFERENT token
    req = MagicMock()
    with (
        patch(
            "api.orchestrator.session.tab_session.TabSession.has_session_token",
            return_value=True,
        ),
        patch(
            "api.orchestrator.session.tab_session.TabSession.extract_session_token",
            return_value="evil-token",
        ),
    ):
        with pytest.raises(SecurityError, match="Hijacked Session Token"):
            session.authenticate_session(req, MagicMock())
