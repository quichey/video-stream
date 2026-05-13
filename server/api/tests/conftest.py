import os
import pytest
from unittest.mock import patch
from sqlalchemy.orm import sessionmaker
from db.Schema import Base
from api.util.db_engine import DataBaseEngine
from api.orchestrator.storage import Storage


# ---------------------------------------------------------
# 1. ENVIRONMENT ORCHESTRATION
# ---------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """
    Surgically patches the Deployment class attribute at the source.
    This ensures db_engine.py sees 'test' regardless of import order.
    """
    from util.env import load_providers_env

    load_providers_env()
    # 1. Start the patcher
    # We point to the specific attribute on the class
    deployment_patcher = patch("util.deployment.Deployment._deployment", "test")
    deployment_env_patcher = patch("util.deployment.Deployment._deployment_env", "test")
    blob_container_patcher = patch(
        "api.orchestrator.storage.Storage.BLOB_CONTAINER", "test"
    )

    # 2. Start the patch
    mock_deployment = deployment_patcher.start()
    mock_deployment_env = deployment_env_patcher.start()
    blob_container_patcher.start()

    # Also set the OS variable just in case other logic relies on it
    old_os_deployment = os.getenv("DEPLOYMENT")
    os.environ["DEPLOYMENT"] = "test"
    old_os_deployment_env = os.getenv("DEPLOYMENT_ENV")
    os.environ["DEPLOYMENT_ENV"] = "test"

    print(f"\n[INFO] Patch Active: Deployment._deployment is now {mock_deployment}")
    print(
        f"\n[INFO] Patch Active: Deployment._deployment_env is now {mock_deployment_env}"
    )

    yield  # --- Tests run here ---

    # 3. Stop the patcher (Teardown)
    deployment_patcher.stop()
    deployment_env_patcher.stop()
    blob_container_patcher.stop()

    if old_os_deployment:
        os.environ["DEPLOYMENT"] = old_os_deployment
    else:
        del os.environ["DEPLOYMENT"]

    if old_os_deployment_env:
        os.environ["DEPLOYMENT_ENV"] = old_os_deployment_env
    else:
        del os.environ["DEPLOYMENT_ENV"]
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


@pytest.fixture
def test_blob_storage():
    storage = Storage()
    test_blobs = []

    def _upload_and_track_video(file_dir, file_name, stream):
        # We track the path so we can delete it later
        test_blobs.append(f"{storage.DIR_VIDEOS}/{file_dir}/{file_name}")
        return storage.store_video(file_dir, file_name, stream)

    def _upload_and_track_image(file_dir, file_name, stream):
        # We track the path so we can delete it later
        test_blobs.append(f"{storage.DIR_IMAGES}/{file_dir}/{file_name}")
        return storage.store_image(file_dir, file_name, stream)

    yield _upload_and_track_video, _upload_and_track_image

    # Cleanup: Delete only the blobs created during this test
    container_client = storage.containter_client
    for blob_path in test_blobs:
        try:
            container_client.delete_blob(blob_path)
        except Exception:
            pass


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
