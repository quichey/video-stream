import os
import pytest
from sqlalchemy.orm import sessionmaker
from db.Schema import Base
from api.util.db_engine import DataBaseEngine


# ---------------------------------------------------------
# 1. ENVIRONMENT ORCHESTRATION
# ---------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """
    Force the environment to 'testing' before any other logic runs.
    This ensures the 'init_engine' logic picks up the simulated specs.
    """
    # Store original state for teardown
    old_env = os.environ.get("APP_ENV")

    # Force the switch
    os.environ["APP_ENV"] = "testing"
    print("\n[INFO] Global Environment set to: TESTING")

    yield  # --- All tests run during this yield ---

    # Restore the environment to avoid side effects on the dev machine
    if old_env:
        os.environ["APP_ENV"] = old_env
    else:
        del os.environ["APP_ENV"]
    print("\n[INFO] Global Environment restored to original state")


# ---------------------------------------------------------
# 2. THE SIMULATED ENGINE & SESSION
# ---------------------------------------------------------
@pytest.fixture(scope="function")
def session():
    """
    Creates an in-memory SQLite database, builds the schema,
    and yields a session. Rolls back/Drops after every test.
    """
    # DataBaseEngine will now use the 'testing' specs due to setup_test_env
    db_manager = DataBaseEngine(deployment="local")
    engine = db_manager.engine

    # Build the tables in RAM
    Base.metadata.create_all(engine)

    # Create the session factory
    SessionLocal = sessionmaker(bind=engine)
    db_session = SessionLocal()

    yield db_session

    # Cleanup to ensure test isolation
    db_session.close()
    Base.metadata.drop_all(engine)


# ---------------------------------------------------------
# 3. PRE-CONDITION DATASETS (SEeding)
# ---------------------------------------------------------
@pytest.fixture
def session_with_user(session):
    """Pre-condition: Database starts with one premium user."""
    # Assuming User model is imported or available
    from db.Schema import User

    user = User(username="kyle_dev", is_premium=True)
    session.add(user)
    session.commit()
    return session


@pytest.fixture
def session_with_video_library(session):
    """Pre-condition: Database starts with 50 videos for testing pagination/lists."""
    from db.Schema import Video

    videos = [Video(title=f"Video {i}") for i in range(50)]
    session.add_all(videos)
    session.commit()
    return session
