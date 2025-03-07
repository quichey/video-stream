from sqlalchemy import create_engine
from sqlalchemy import text


class DB_CONNECTOR():

    def __init__(self,
                dialect,
                db_api,
                user,
                pw,
                hostname,
                dbname,
                ):

        url = f"{user}:{pw}@{hostname}/{dbname}"
        self.engine = create_engine(f"{dialect}+{db_api}://{url}", echo=True)    


    def create_database(self):
        pass

    def create_table(self):
        pass

    def populate_table(self, table):
        pass

    def seed_db(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("select 'hello world'"))
            print(result.all())
            # create_database
            # create_table(s)
            # populate_tables
            # maybe save a backup of database as archive copy of state
    
        pass