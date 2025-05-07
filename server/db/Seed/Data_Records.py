import random
import time

from datetime import datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy import Boolean, Integer, String, DateTime
from sqlalchemy.orm import Session

class Data_Records():
    def __init__(self, seed):
        self.seed = seed

    
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
            if self.seed.is_a_primary_key(table, key):
                continue


            print(f"\n\n  table {table.name} creating column: {key} \n\n")
            column = getattr(table.c, key)
            record[key] = self.seed.create_random_value(column)
        # probably convert record dictionary into sqlalchemy Record object type
        # maybe not if the insert function only requires a list of dicts
        
        #TODO: check out to dynamically create a class from a variable class name
        record = self.seed.schema.get_record_factory(table.name)(**record)
        return record      

    def is_foreign_key(self, column):
        return len(column.foreign_keys) > 0
    
    def get_random_foreign_key(self, column):
        # TODO: check self.seed.cache for the primary keys

        # get len() of cached table
        # do random.int of index of table to get random record
        # get that record's id

        # add function to backup db if it already exists 
        # like i did at ISS
        pass


    def create_random_value(self, column):
        data_type = column.type
        print(f"\n\n data_type: {data_type} \n\n")
        column_name = column.name
        table_name = column.table.name


        #if is_foreign_key:
        if self.seed.is_foreign_key(column):
            # scan parent table
            # use metadata obj to query other table
            #return self.seed.get_random_foreign_key(column)
            fk_curr = self.seed.get_random_foreign_key(column)
            print(f"\n\n fk_curr: {fk_curr} \n\n")
            """
                fk_curr: {'id': 2}
                return fk_curr[fk_info["fk_column_name"]]

                need to save fk_info["fk_column_name"] from previous for loop
                i think this is fine. 
            """
            foreign_key_name = "blah"
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


    def init_table_data(self, list_of_table_rand):

        
        with Session(self.seed.engine) as session:
            # if i keep this cache object, I dont have to do
            # select queries assuming every record gets
            # correctly inserted
            # what should i do if this assumption fails?
            # TODO: answer above question
            self.seed.cache = {}
            for table_state in list_of_table_rand:
                self.seed.cache[table_state.name] = []
                table_instance = self.seed.get_table_metadata(table_state.name)
                for _ in range(table_state.num_records):
                    random_record = self.seed.create_random_record(table_instance)
                    self.seed.cache[table_state.name].append(random_record)
                    session.add(random_record)
            
            session.commit()
        
        return
    

    
        
        # - and then create original ddl

        
