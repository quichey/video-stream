import os
from db.Schema import User


def test_is_using_simulated_db(session):
    """
    Verify we are in the 'testing' environment and
    the database is empty/isolated.
    """
    # 1. Check the environment flag
    assert os.getenv("DEPLOYMENT") == "test"

    # 2. Check that the DB is actually SQLite (the simulation)
    # The 'bind' is the engine connected to the session
    assert "sqlite" in str(session.bind.url)

    # 3. Verify it's empty
    assert session.query(User).count() == 0


def test_data_isolation(session):
    """
    Verify that data from one test doesn't leak into the next.
    """
    new_user = User(name="kyle_dev")
    session.add(new_user)
    session.commit()
    assert session.query(User).count() == 1


# When Pytest runs a third test after this, the count should be 0 again.
