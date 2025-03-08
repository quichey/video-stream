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