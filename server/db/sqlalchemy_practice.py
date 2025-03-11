from sqlalchemy import create_engine
from sqlalchemy import text

from db.DB_CONNECTOR import DB_CONNECTOR
from db.DB_SCHEMA import database_specs


# create engine
def start_engine():
    dialect = "mysql"
    db_api = "mysqlconnector"

    user = "new_user"
    pw = "password"
    hostname = "localhost:3306"
    dbname = "video_stream"
    url = f"{user}:{pw}@{hostname}/{dbname}"

    engine = create_engine(f"{dialect}+{db_api}://{url}", echo=True)
    return engine


def connect_engine(engine):
    with engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        print(result.all())


def commit_changes():
    engine = start_engine()
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()


def fetch_rows():
    engine = start_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for row in result:
            print(f"x: {row.x}  y: {row.y}")


def bind_parameters():
    engine = start_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
        for row in result:
            print(f"x: {row.x}  y: {row.y}")


def bind_multi_parameters():
    engine = start_engine()
    # instead of .connect, I can do .begin and then forego the last .commit statement, iirc
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
        )
        conn.commit()


from sqlalchemy.orm import Session

def test_session():
    engine = start_engine()
    stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
    with Session(engine) as session:
        result = session.execute(stmt, {"y": 6})
        for row in result:
            print(f"x: {row.x}  y: {row.y}")


def test_session_update():
    engine = start_engine()
    with Session(engine) as session:
        result = session.execute(
            text("UPDATE some_table SET y=:y WHERE x=:x"),
            [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
        )
        session.commit()