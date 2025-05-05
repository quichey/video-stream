import random
import time

from datetime import datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy import create_engine
from sqlalchemy import insert, select
from sqlalchemy import Boolean, Integer, String, DateTime
from sqlalchemy.orm import Session


#Sketching out blueprint/concepts of Seed class vs Cache class
"""
I want the Seed class to be a wrapper around the sqlalchemy library, to be able to quickly create test data-sets for a given schema.

I want the Cache class to be an internal Encapsulation within the Seed class,
to store any important information of the state of database during the process of populating test data

Why am i doing this?
Auto-populating foreign keys based off the parent table's primary keys is seeming to be difficult.
And this is without handling the case of composite foreign/primary key defs.

But i am unclear of what internal state the Seed class should have as opposed to putting them in the Cache class.
I think the Seed class should have the sqlalchemy constructs/objects, but the cache seems to be using sqlalchemy queries
in order to populate data. This may be fine.
The Seed class mainly has the programs/functions to run on the command-line that actually create the data.
The user of the Seed program should not have to know sqlalchemy queries.

The Seed class can handle the different script options/configs, while the cache class can handle the sqlalchemy calls, when it needs to.
This seems like the Cache class will have a ton of functions.
Should i move it to a different file? I think so.
Pros?
- idk
Cons?
- idk
probably not important

I think what i need to do next is create update_cache_* functions within cache,
or seems just moving over any function with self.cache into cache seems to make more sense.
But I feel lazy right now
"""


@dataclass
class TableTestingState:
    """Class for keeping track of an test dataset table generation info."""
    "name": str
    "num_records": int

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
    base = None
    metadata_obj = None
    engine = None


    def __init__(self, admin_specs, database_specs, schema):
        self.admin_specs = admin_specs
        self.database_specs = database_specs
        self.schema = schema
        self.base = schema.Base
        self.metadata_obj = schema.Base.metadata
        self.construct_engine()
        self.construct_admin_engine()

    def get_table_metadata(self, table_name):
        return self.metadata_obj.tables[table_name]
    

    def parse_test_data_file(self):
        # first row is table name
        # second row is columns names
        # determine the delimiter
        # construct list of dictionary records
        pass
    
    def fill_table_with_test_data(self, table_name, test_file):
        pass
    

    def construct_engine(self):
        database_specs = self.database_specs
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
    
    
    def construct_admin_engine(self):
        admin_specs = self.admin_specs
        dialect = admin_specs["dialect"]
        db_api = admin_specs["db_api"]

        user = admin_specs["user"]
        pw = admin_specs["pw"]
        hostname = admin_specs["hostname"]
        dbname = admin_specs["dbname"]
        url = f"{user}:{pw}@{hostname}/{dbname}"

        engine = create_engine(f"{dialect}+{db_api}://{url}", echo=True)
        self.admin_engine = engine
        return engine

    # Creates the database if not exists as well as the empty tables
    def create_database_definition(self):
        self.metadata_obj.create_all(self.engine)
        return
    
    def is_a_primary_key(self, table, key):
        # think may change comments to not have id later
        # but actually do need it because
        # a user can comment multiple times on a video
        return key == "id"

    def create_random_record(self, table):
        # get table specs for table object
        # get column names and column types
        # use create_random_value
        # sqlalchemy may have function available to do this
        record = {"id": None}
        
        keys = table.c.keys()
        for key in keys:
            if self.is_a_primary_key(table, key):
                continue


            print(f"\n\n  table {table.name} creating column: {key} \n\n")
            column = getattr(table.c, key)
            record[key] = self.create_random_value(column)
        # probably convert record dictionary into sqlalchemy Record object type
        # maybe not if the insert function only requires a list of dicts
        
        #TODO: check out to dynamically create a class from a variable class name
        record = self.schema.get_record_factory(table.name)(**record)
        return record      

    def is_foreign_key(self, column):
        return len(column.foreign_keys) > 0
    
    def get_random_foreign_key(self, column):
        # TODO: check self.cache for the primary keys

        # get len() of cached table
        # do random.int of index of table to get random record
        # get that record's id

        # add function to backup db if it already exists 
        # like i did at ISS
        pass

    def back_up_db(self):
        # TODO: lookup sqlalchemy way to do it
        # for inter-operability b/t db engines
        return

    def create_random_value(self, column):
        data_type = column.type
        print(f"\n\n data_type: {data_type} \n\n")
        column_name = column.name
        table_name = column.table.name


        #if is_foreign_key:
        if self.is_foreign_key(column):
            # scan parent table
            # use metadata obj to query other table
            #return self.get_random_foreign_key(column)
            fk_curr = self.get_random_foreign_key(column)
            print(f"\n\n fk_curr: {fk_curr} \n\n")
            """
                fk_curr: {'id': 2}
                return fk_curr[fk_info["fk_column_name"]]

                need to save fk_info["fk_column_name"] from previous for loop
                i think this is fine. 
            """
            return fk_curr[foreign_key_name]
        
        def random_date(start_date, end_date):
            start_timestamp = time.mktime(start_date.timetuple())
            end_timestamp = time.mktime(end_date.timetuple())
            random_timestamp = random.uniform(start_timestamp, end_timestamp)
            return datetime.fromtimestamp(random_timestamp)
        hardcoded_end_date = datetime.now()
        hardcoded_start_date = hardcoded_end_date - relativedelta(years=10)


        if isinstance(data_type, Boolean):
            flag = random.randint(0, 1)
            return True if flag == 1 else False
        
        elif isinstance(data_type, Integer):
            return random.randint(0, 10000)
        
        elif isinstance(data_type, String):
            rand_int = random.randint(0, 10000)
            return f"{table_name}_{column_name}_{rand_int}"
        
        elif isinstance(data_type, DateTime):
            return random_date(hardcoded_start_date, hardcoded_end_date)


    def init_db(self, list_of_table_rand):

        
        with Session(self.engine) as session:
            # if i keep this cache object, I dont have to do
            # select queries assuming every record gets
            # correctly inserted
            # what should i do if this assumption fails?
            # TODO: answer above question
            self.cache = {}
            for table_state in list_of_table_rand:
                self.cache[table_state["name"]] = []
                for _ in range(table_state.num_records):
                    random_record = self.create_random_record()
                    self.cache[table_state["name"]].append(random_record)
                    session.add(random_record)
            
            session.commit()
        
        return

    # fill in tables with given test data
    # TODO: update, i think create TableTestState instances here or in load_db.py
    def initiate_test_environment(self, testing_state):
        self.create_database_definition()

        print(f"testing_state: {testing_state}")
        list_of_table_files = testing_state.get("table_files", {})
        for file in list_of_table_files:
            table_data = self.parse_test_data_file(file)
            print(f"table_data: {table_data}")
        list_of_table_rand = testing_state["tables_random_populate"]

        self.back_up_db()
        self.init_db(list_of_table_rand)
 

# ideas for testing state
# fill up users table with random data since it does not have foreign keys
# and then view contents
# and then write up test files for other tables using id's from this table
# -- possibly add in a case in create_random_data where it checks if the column
# -- is a foreign key, and then scan the parent table for a proper id