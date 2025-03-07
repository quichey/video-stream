from sqlalchemy import create_engine
from sqlalchemy import text


class DB_CONNECTOR():

    def __init__(self):
        pass
    
    def create_database(self):
        pass

    def create_table(self):
        pass

    def populate_table(self, table):
        pass

    def seed_db(self):
        # create_database
        # create_table(s)
        # populate_tables
        # maybe save a backup of database as archive copy of state
        pass

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