import os
import pytest
from unittest.mock import patch
from sqlalchemy.orm import sessionmaker
from db.Schema import Base
from api.util.db_engine import DataBaseEngine


# ---------------------------------------------------------
# 1. ENVIRONMENT ORCHESTRATION
# ---------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """
    Surgically patches the Deployment class attribute at the source.
    This ensures db_engine.py sees 'test' regardless of import order.
    """
    # 1. Start the patcher
    # We point to the specific attribute on the class
    patcher = patch("util.deployment.Deployment._deployment", "test")

    # 2. Start the patch
    mock_deployment = patcher.start()

    # Also set the OS variable just in case other logic relies on it
    old_os_env = os.getenv("DEPLOYMENT")
    os.environ["DEPLOYMENT"] = "test"

    print(f"\n[INFO] Patch Active: Deployment._deployment is now {mock_deployment}")

    yield  # --- Tests run here ---

    # 3. Stop the patcher (Teardown)
    patcher.stop()

    if old_os_env:
        os.environ["DEPLOYMENT"] = old_os_env
    else:
        del os.environ["DEPLOYMENT"]
    print("\n[INFO] Patch Stopped: Environment restored.")


# ---------------------------------------------------------
# 2. THE SIMULATED ENGINE & SESSION
# ---------------------------------------------------------
@pytest.fixture(scope="function")
def session():
    """
    Now DataBaseEngine will absolutely see 'test' when it
    accesses self.deployment.
    """
    db_manager = DataBaseEngine()
    engine = db_manager.engine

    # Verify the engine is SQLite before proceeding
    if "sqlite" not in str(engine.url):
        raise RuntimeError(f"Safety Trigger: Test tried to run on {engine.url}!")

    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db_session = SessionLocal()

    yield db_session

    db_session.close()
    Base.metadata.drop_all(engine)


# ---------------------------------------------------------
# 3. PRE-CONDITION DATASETS (SEeding)
# ---------------------------------------------------------
@pytest.fixture
def session_with_user(session):
    """Pre-condition: Database starts with one test user."""
    from db.Schema import User

    # Create a user matching your specific schema
    # Using .encode() because your password column is VARBINARY
    test_user = User(
        name="kyle_dev",
        email="kyle@example.com",
        profile_icon="default.png",
        password=b"hashed_password_blob",
    )

    session.add(test_user)
    session.commit()

    # We return the user object so your test can use test_user.id immediately
    return test_user


@pytest.fixture
def session_with_video_library(session):
    """Pre-condition: Database starts with 50 videos for testing pagination/lists."""
    from db.Schema import Video

    videos = [Video(title=f"Video {i}") for i in range(50)]
    session.add_all(videos)
    session.commit()
    return session
