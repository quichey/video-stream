import random

from dataclasses import dataclass

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Boolean, Integer, String

"""
@dataclass
class PK_Def:
    #Class for storing set of all primary keys for a table
    table: Table
    pk_list: set

@dataclass
class PK_Values:
    #Class for storing set of all primary keys for a table
    table: Table
    pk_list: set
"""

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

        # name is table_name, value is name of primary key column (or or list of col names if multi-col pk)
        self.pk_definitions = {}
        # name is table_name, value is list of fk columns (name of column and parent table)
        self.fk_references = {}
        # name is table_name, value is set of primary-key values
        self.pk_values = {}
        # name is table_name, value is set of foreign-key values (also primary key if multi-col pk)
        self.fk_values = {}
    

    def get_table_key_values(self, table_instance):
        table_name = table_instance.name
        if table_name in self.pk_values.keys():
            return self.pk_values[table_name]
        # i think use the Session class
        # and do table_instance.select("id")
        pass

    def get_table_key_definition(self, table_instance):
        table_name = table_instance.name
        if table_name in self.pk_definitions.keys():
            return self.pk_definitions[table_name]

        pk = table_instance.primary_key
        pk_defs = []
        for column in pk.columns:
            pk_defs.append(column.name)

        self.pk_definitions[table_name] = pk_defs
        return pk_defs


    def get_table_metadata(self, table_name):
        return self.metadata_obj.tables[table_name]
    
    # just noticed
    # foreign_key values
    # are actually primary_keys for "complex" tables (multi-col pk tables)
    def get_foreign_key_values(self, table_instance):
        table_name = table_instance.name
        if table_name in self.fk_values.keys():
            return self.fk_values[table_name]
        pass

    def get_foreign_key_references(self, table_instance):
        child_table_name = table_instance.name
        if child_table_name in self.fk_references.keys():
            return self.fk_references[child_table_name]

        fks = table_instance.foreign_key_constraints
        fk_reference_info_list = []
        for fk in fks:
            one_info = {}

            for column in fk.columns:
                one_info["column_name"] = column.name
            
            parent_table_name = fk.referred_table.name
            one_info["table_name"] = fk.referred_table.name

            parent_table = self.get_table_metadata(parent_table_name)
            one_info["foreign_key_values"] = self.get_table_key_values(parent_table)

            fk_reference_info_list.append(one_info)
        

        self.fk_references[child_table_name] = fk_reference_info_list
        return fk_reference_info_list
    

    def parse_test_data_file(self):
        # first row is table name
        # second row is columns names
        # determine the delimiter
        # construct list of dictionary records
        pass
    
    def fill_table_with_test_data(self, table_name, test_file):
        pass
    

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
    

    def create_pk(self, table, column_name):
        # check through list of already existing pk's
        # make a new one
        # 
        pass
    
    def get_random_foreign_key(self, column):
        pass

    def create_random_value(self, column):
        # check sqlalchemy docs for proper way to get data_type of column and name
        data_type = pass
        column_name = pass
        table_name = pass

        is_foreign_key = pass
        if is_foreign_key:
            # scan parent table
            # use metadata obj to query other table
            return self.get_random_foreign_key(column)

        # do case switch on data_type
        match type(data_type):
            case Boolean:
                flag = random.randint(0, 1)
                return True if flag == 1 else False
            case Integer:
                return random.randint(0, 10000)
            case String:
                rand_int = random.randint(0, 10000)
                return f"{table_name}_{column_name}_{rand_int}"


    def initialize_random_record(self, table):

        # need to alter a bit to do the case of comment_likes table
        # pk is multiple columns
        # so create_pk should return not just a single value
        # but a dictionary with each column name mapped to a fk value
        # and then set record to this dictionary
        pk_def = self.get_table_key_definition(table)
        record = {}
        # check for valid fk values
        # 
        for key in pk_def:
            record[key] = self.create_pk(table, key)
    
        return record
    
    def is_a_primary_key(self, table, column_name):
        pk_def = self.get_table_key_definition(table)
        if type(pk_def) == list:
            return column_name in pk_def
        else:
            return column_name == pk_def

    def create_random_record(self, table):
        # get table specs for table object
        # get column names and column types
        # use create_random_value
        # sqlalchemy may have function available to do this
        record = self.initialize_random_record(table)
        
        keys = table.c.keys()
        for key in keys:
            if self.is_a_primary_key(table, key):
                continue
            column = getattr(table.c, key)
            record[key] = self.create_random_value(column)
        # probably convert record dictionary into sqlalchemy Record object type
        # maybe not if the insert function only requires a list of dicts
        return record


    # Creates the database if not exists as well as the empty tables
    def create_database_definition(self):
        self.metadata_obj.create_all(self.engine)
        pass

    # fill in tables with given test data
    def initiate_test_environment(self, testing_state):
        list_of_table_files = testing_state["table_files"]
        list_of_table_rand = testing_state["table_random_populate"]
        for file in list_of_table_files:
            table_data = self.parse_test_data_file(file)
        
        for table_info in list_of_table_rand:
            # populate table with random data
            num_records = table_info["num_records"]
            table_name = table_info["name"]
            table = self.get_table_metadata(table_name)
            records = []
            for i in range(num_records):
                records.append(self.create_random_record(table))

        pass

# ideas for testing state
# fill up users table with random data since it does not have foreign keys
# and then view contents
# and then write up test files for other tables using id's from this table
# -- possibly add in a case in create_random_data where it checks if the column
# -- is a foreign key, and then scan the parent table for a proper id