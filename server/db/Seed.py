self.import random

from dataclasses import dataclass

from sqlalchemy import create_engine
from sqlalchemy import select
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
    database_specs = None
    metadata_obj = None
    engine = None

    pk_definitions = {}
    # initialize the pk_definitions since we already have schema
    # init these caches, but I want to get data for these at the time of test-data creation
    # name is table_name, value is list of fk columns (name of column and parent table)
    fk_references = {}
    # name is table_name, value is set of primary-key values
    # TODO: think of at what instances i need to clear these caches
    # in terms of the use-cases of this Seed Class
    pk_values = {}
    # name is table_name, value is set of foreign-key values (also primary key if multi-col pk)
    fk_values_possible = {}
    fk_values_existing = {}
    # populate fk_values_existing with empty lists for each table


    def __init__(self, database_specs=database_specs, metadata_obj=metadata_obj):
        self.database_specs = database_specs
        self.metadata_obj = metadata_obj
        self.construct_engine(database_specs)

        # initialize the pk_definitions since we already have schema
        self.init_pk_definitions()
        # populate fk_values_existing with empty lists for each table
        self.init_fk_values_existing()
    
    def init_pk_definitions(self):
        all_tables = self.metadata_obj.tables.values()
        for table_instance in all_tables:
            self.get_table_key_definition(table_instance)
        
    def init_fk_values_existing(self):
        all_tables = self.metadata_obj.tables.keys()
        for table_name in all_tables:
            self.fk_values_existing[table_name] = []

    def get_random_foreign_key(self, table_instance):
        parent_table_name = self.fk_references[table_instance.name][0]["table_name"]
        parent_table = self.get_table_metadata(parent_table_name)

        pk_values = self.get_table_key_values(parent_table)
        num_vals = len(pk_values)
        random_idx = random.randint(0, num_vals - 1)
        return pk_values[random_idx]
        

    def get_table_key_values(self, table_instance):
        table_name = table_instance.name
        if table_name in self.pk_values.keys():
            return self.pk_values[table_name]

        pk_col_name = self.pk_definitions[table_name]
        pk_col = getattr(table_instance.c, pk_col_name)
        stmt = select(pk_col)
        values = []
        with self.engine.connect() as conn:
            records = conn.execute(stmt)
            for row in records:
                val = {}
                val[pk_col_name] = row[pk_col_name]
                values.append(val)
        self.pk_values[table_name] = values
        return values


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
    def get_foreign_key_values_possible(self, table_instance):
        table_name = table_instance.name
        if table_name in self.fk_values_possible.keys():
            return self.fk_values_possible[table_name]
        
        fk_references = self.get_foreign_key_references(table_instance)
        possible = []
        # doing bfs (breadth-first-search)
        def traverse_references(idx, fk_dict_so_far):
            if idx >= len(fk_references):
                return
            ref = fk_references[idx]
            pk = ref["column_name"]
            pk_values = ref["foreign_key_values"]
            
            for val in pk_values:
                fk_dict = dict(fk_dict_so_far)
                fk_dict[pk] = val

                if idx == len(fk_references) - 1:
                    possible.append(fk_dict)
                else:
                    traverse_references(idx + 1, fk_dict)
            
        empty_fk = {}
        traverse_references(0, empty_fk)

        self.fk_values_possible[table_name] = possible
        return possible

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
    

    def initialize_random_record_simple_pk(self, table):
        # check through list of already existing pk's
        # make a new one
        existing_values = self.get_table_key_values(table)
        i = 0
        found_new_value = False
        while i in existing_values:
            i += 1
        pk_name = self.get_table_key_definition(table)[0]
        record = {}
        record[pk_name] = i
        return record
    
    
    def initialize_random_record_compound_pk(self, table)
        fk_values_possible = self.get_foreign_key_values_possible(table)
        fk_values_existing = self.foreign_key_values_existing[table]

        for fk in fk_values_possible:
            already_exists = False
            for fk_2 in fk_values_existing:
                if fk == fk_2:
                    already_exists = True
                    break
            if already_exists:
                continue
    
            # add fk to fk_values_existing
            fk_values_existing.append(fk)
            return fk
    

    def create_random_value(self, column):
        # check sqlalchemy docs for proper way to get data_type of column and name
        # TODO: fill in getting these values
        data_type = pass
        column_name = pass
        table_name = pass

        is_foreign_key = pass
        if is_foreign_key:
            # scan parent table
            # use metadata obj to query other table
            return self.get_random_foreign_key(column)

        # do case switch on data_type
        # TODO: do a case for datetime
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
        # try simplifying cases into single col pk and multi-col pk

        # need to alter a bit to do the case of comment_likes table
        # pk is multiple columns
        # so create_pk should return not just a single value
        # but a dictionary with each column name mapped to a fk value
        # and then set record to this dictionary
        pk_def = self.get_table_key_definition(table)

        if len(pk_def) == 1:
            return self.initialize_random_record_simple_pk(table)
        else:
            return self.initialize_random_record_compound_pk(table)
    
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
        for file in list_of_table_files:
            table_data = self.parse_test_data_file(file)
        list_of_table_rand = testing_state["table_random_populate"]
        
        for table_info in list_of_table_rand:
            # populate table with random data
            num_records = table_info["num_records"]
            table_name = table_info["name"]
            table = self.get_table_metadata(table_name)
            records = []
            for i in range(num_records):
                records.append(self.create_random_record(table))
            # TODO: do insert statements with all the random records

        pass
        
    

# ideas for testing state
# fill up users table with random data since it does not have foreign keys
# and then view contents
# and then write up test files for other tables using id's from this table
# -- possibly add in a case in create_random_data where it checks if the column
# -- is a foreign key, and then scan the parent table for a proper id