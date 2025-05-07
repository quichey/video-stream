
import sqlalchemy as sql
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


"""
GUNAM SEED, though i didn't actually watch that one
G Gundam is better though humorously racist
"""

class Data_Base_Structure():
    def __init__(self, seed):
        self.seed = seed
        self.back_up_counter = 0
        self.construct_engine()
        self.construct_admin_engine()

    @property
    def back_up_db_name(self):
        return f"{self.database_specs.dbname}_{self.back_up_counter}"

    def init_ddl(self):
        with Session(self.seed.admin_engine) as admin_session:
            db_name = self.seed.database_specs.dbname
            query = "SHOW DATABASES"
            db_records = admin_session.execute(sql.text(query))
            exists = False
            for r in db_records:
                if r[0] == db_name:
                    exists = True
                elif db_name in r[0]:
                    self.seed.back_up_counter = self.seed.back_up_counter + 1

            if exists:
                self.back_up_db(self.seed, admin_session)
            self.create_database_definition(self.seed)
        return


    # Creates the database if not exists as well as the empty tables
    def create_database_definition(self, engine=None):
        if engine is None:
            engine = self.seed.engine
        print(f"\n\n creating ddl: {engine} \n\n")
        self.seed.metadata_obj.create_all(engine)

        return


    """
    TODO: ?
    may need or want to get rid of database_specs to
    avoid/deal-with concurrency problems.
    or finally understand python multithreading library
    """
    def back_up_db(self, admin_session):
        back_up_db_name = self.seed.back_up_db_name
        self.seed.create_database(admin_session, back_up_db_name)
        back_up_engine = self.seed.construct_back_up_engine()
        self.seed.create_database_definition(back_up_engine)

        #TODO:
        # - check for concurrency problems
        dialect = self.seed.admin_specs.dialect
        db_name = self.seed.database_specs.dbname
        query = ""
        match dialect:
            case "mysql":
                query = f"DROP DATABASE {db_name}"
        admin_session.execute(sql.text(query))
        return


    def create_database(self, admin_session, db_name):
        dialect = self.seed.admin_specs.dialect
        query = ""
        match dialect:
            case "mysql":
                query = f"CREATE DATABASE {db_name}"
        admin_session.execute(sql.text(query))
        return


    def construct_back_up_engine(self):
        db_specs = self.seed.admin_specs
        db_specs.dbname = self.seed.back_up_db_name
        conn_str = self.seed.construct_db_conn_str(db_specs)

        engine = create_engine(conn_str, echo=True)
        return engine


    def construct_engine(self):
        conn_str = self.seed.construct_db_conn_str(self.seed.database_specs)

        engine = create_engine(conn_str, echo=True)
        self.seed.engine = engine
        return engine


    def construct_admin_engine(self):
        conn_str = self.seed.construct_db_conn_str(self.seed.admin_specs)

        engine = create_engine(conn_str, echo=True)
        self.seed.admin_engine = engine
        return engine


    def construct_db_conn_str(self, database_specs):
        dialect = database_specs.dialect
        db_api = database_specs.db_api

        user = database_specs.user
        pw = database_specs.pw
        hostname = database_specs.hostname
        dbname = database_specs.dbname 
        url = f"{dialect}+{db_api}://{user}:{pw}@{hostname}"
        if dbname != "":
            url += f"/{dbname}"
        return url
