import random

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Boolean, Integer, String


# may expand this file to be named snapshot_db
# to draw inspiration from ISS/Clinicomp as well as the
# glorious game Pokemon Snap
# -- ideally i would make functionality to
# - Check if database named video_stream exists
# - - if not, create it with a test user
# - create/load tables with demo-able data
# - prepare indices for optimal searching/fetching for appropriate cases

class Seed():
    def __init__(self, database_specs=database_specs, metadata_obj=metadata_obj):
        self.database_specs = database_specs
        self.metadata_obj = metadata_obj
        self.construct_engine(database_specs)
    

    def construct_engine(self, database_specs):
        dialect = database_specs["dialect"]
        db_api = database_specs["db_api"]

        user = database_specs["user"]
        pw = database_specs["pw"]
        hostname = database_specs["hostname"]
        dbname = database_specs["dbname"]
        url = f"{user}:{pw}@{hostname}/{dbname}"

        engine = create_engine(f"{dialect}+{db_api}://{url}", echo=True)
        self.engine = engine
        return engine
    

    def create_random_value(self, data_type, table_name=None, column_name=None):
        # do case switch on data_type
        match type(data_type):
            case Boolean
                flag = random.randint(0, 1)
                return True if flag == 1 else False
            case Integer
                return random.randint(0, 10000)
            case String
                rand_int = random.randint(0, 10000)
                return f"{table_name}_{column_name}_{rand_int}"


    def create_random_record(self, table):
        # get table specs for table object
        # get column names and column types
        # use create_random_value
        # sqlalchemy may have function available to do this
        record = {}

        unique_id = pass
        table_name = pass # check docs for proper way of getting table name
        keys = table.c.keys()
        for key in keys:
            column_info = getattr(table.c, key)
            # check sqlalchemy docs for proper way to get data_type of column and name
            data_type = pass
            column_name = pass
            record[key] = self.create_random_value(data_type, table_name, column_name)
        # probably convert record dictionary into sqlalchemy Record object type
        # maybe not if the insert function only requires a list of dicts
        return record


    # Creates the database if not exists as well as the empty tables
    def create_database_definition(self):
        self.metadata_obj.create_all(self.engine)
        pass

    # fill in tables with given test data
    def initiate_test_environment(self, testing_state):
        pass