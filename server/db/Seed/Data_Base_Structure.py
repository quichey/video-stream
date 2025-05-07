
import sqlalchemy as sql
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


"""
GUNAM SEED, though i didn't actually watch that one
G Gundam is better though humorously racist
"""

class Data_Base_Structure():
    def init_ddl(seed):
        with Session(seed.admin_engine) as admin_session:
            db_name = seed.database_specs.dbname
            query = "SHOW DATABASES"
            db_records = admin_session.execute(sql.text(query))
            exists = False
            for r in db_records:
                if r[0] == db_name:
                    exists = True
                elif db_name in r[0]:
                    seed.back_up_counter = seed.back_up_counter + 1

            if exists:
                back_up_db(seed, admin_session)
            create_database_definition(seed)
        return


    # Creates the database if not exists as well as the empty tables
    def create_database_definition(seed, engine=None):
        if engine is None:
            engine = seed.engine
        print(f"\n\n creating ddl: {engine} \n\n")
        seed.metadata_obj.create_all(engine)

        return


    """
    TODO: ?
    may need or want to get rid of database_specs to
    avoid/deal-with concurrency problems.
    or finally understand python multithreading library
    """
    def back_up_db(seed, admin_session):
        back_up_db_name = seed.back_up_db_name
        seed.create_database(admin_session, back_up_db_name)
        back_up_engine = seed.construct_back_up_engine()
        seed.create_database_definition(back_up_engine)

        #TODO:
        # - check for concurrency problems
        dialect = seed.admin_specs.dialect
        db_name = seed.database_specs.dbname
        query = ""
        match dialect:
            case "mysql":
                query = f"DROP DATABASE {db_name}"
        admin_session.execute(sql.text(query))
        return


    def create_database(seed, admin_session, db_name):
        dialect = seed.admin_specs.dialect
        query = ""
        match dialect:
            case "mysql":
                query = f"CREATE DATABASE {db_name}"
        admin_session.execute(sql.text(query))
        return


    def construct_back_up_engine(seed):
        db_specs = seed.admin_specs
        db_specs.dbname = seed.back_up_db_name
        conn_str = seed.construct_db_conn_str(db_specs)

        engine = create_engine(conn_str, echo=True)
        return engine


    def construct_engine(seed):
        conn_str = seed.construct_db_conn_str(seed.database_specs)

        engine = create_engine(conn_str, echo=True)
        seed.engine = engine
        return engine


    def construct_admin_engine(seed):
        conn_str = seed.construct_db_conn_str(seed.admin_specs)

        engine = create_engine(conn_str, echo=True)
        seed.admin_engine = engine
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
