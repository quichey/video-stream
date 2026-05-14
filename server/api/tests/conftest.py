import os
import pytest
import json
from unittest.mock import patch
from sqlalchemy.orm import sessionmaker
from db.Schema import Base, test_database_specs
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

    # If the file exists from a crashed previous run, delete it for a clean start
    test_db_path = test_database_specs["dbname"]
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

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
def session_old():
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


@pytest.fixture(scope="function")
def session():
    """
    Seeding/Cleanup session. Points to the SAME engine as the app
    because DataBaseEngine is governed by the same session patches.
    """
    db_manager = DataBaseEngine()
    engine = db_manager.engine
    # MANDATORY: Re-run create_all.
    # SQLAlchemy's create_all is idempotent; it won't break anything if
    # the tables exist, but it ENSURES they exist for this specific connection.
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    db_session = SessionLocal()

    yield db_session

    db_session.close()

    # Clean up data after every test to keep isolation,
    # but leave the tables (metadata) intact for the session-scoped app.
    with engine.connect() as connection:
        transaction = connection.begin()
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())
        transaction.commit()


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


@pytest.fixture(scope="session")
def app(setup_test_env):
    """
    Initializes the schema once and creates the Flask app.
    The 'setup_test_env' dependency ensures patches are active.
    """
    # 1. Initialize the shared Test Database
    db_manager = DataBaseEngine()
    engine = db_manager.engine

    if "sqlite" not in str(engine.url):
        raise RuntimeError(
            f"CRITICAL: App tried to connect to production! {engine.url}"
        )

    # 2. Build the schema once for the entire session
    Base.metadata.create_all(engine)

    # 3. Create the Flask App
    from api.gateway import create_app

    flask_app = create_app({"TESTING": True})

    yield flask_app

    # Optional: Clean up the file/memory after all tests finish
    # Base.metadata.drop_all(engine)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


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


@pytest.fixture
def load_state(app):
    def _loader(state_name):
        from api.util.db_engine import DataBaseEngine
        from sqlalchemy.orm import sessionmaker

        # 1. Map table names to model classes dynamically
        # Base.registry.mappers gives us access to all mapped classes
        table_to_model = {
            mapper.class_.__tablename__: mapper.class_
            for mapper in Base.registry.mappers
        }

        # 2. Load the JSON state file
        file_path = f"api/tests/states/{state_name}.json"
        with open(file_path, "r") as f:
            data = json.load(f)

        # 3. Connect and Seed
        engine = DataBaseEngine().engine
        Session = sessionmaker(bind=engine)

        with Session() as session:
            for table_name, rows in data.items():
                model_class = table_to_model.get(table_name)

                if not model_class:
                    print(f"[WARNING] No model found for table: {table_name}")
                    continue

                for row_data in rows:
                    session.add(model_class(**row_data))

            session.commit()

    return _loader
