import random
import time
import os

from datetime import datetime
from dateutil.relativedelta import relativedelta

from sqlalchemy import Boolean, Integer, String, DateTime
from sqlalchemy.orm import Session


from db.Schema.Video import VideoFileManager




class Data_Records():
    # dict of "table_name": SqlAlchemy Base class
    cache = {}

    def __init__(self, seed):
        self.seed = seed
        self.video_file_manager = VideoFileManager()

    
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

            column = getattr(table.c, key)
            if self.is_foreign_key(column):
                continue

            special_cases = [
                "file_dir", #videos
            ]
            # for video storage
            if key in special_cases:
                continue

            record[key] = self.create_random_value(column)
        # probably convert record dictionary into sqlalchemy Record object type
        # maybe not if the insert function only requires a list of dicts


        #TODO: check out to dynamically create a class from a variable class name
        record = self.insert_foreign_keys(table, record)
        record = self.seed.schema.get_record_factory(table.name)(**record)
        if table.name == "videos":
            self.video_file_manager.store_video(record)
        return record      

    def insert_foreign_keys(self, table, record):
        keys = table.c.keys()
        for key in keys:
            column = getattr(table.c, key)
            if not self.is_foreign_key(column):
                continue
            fk_curr = self.get_random_foreign_key(column)
            print(f"\n\n  table {table.name} creating fk: {key} -- {fk_curr} \n\n")
            record[key] = fk_curr

        return record

    def is_foreign_key(self, column):
        return len(column.foreign_keys) > 0
    
    def get_random_foreign_key(self, column):
        # TODO: check self.cache for the primary keys
        cache = self.cache
        referred_table_name = None
        for fk in column.foreign_keys:
            constraint = fk.constraint
            referred_table_name = constraint.referred_table.name

        # get len() of cached table
        # do random.int of index of table to get random record
        # get that record's id
        records = cache[referred_table_name]
        random_idx = random.randint(0, len(records) - 1)
        return records[random_idx].id


    def create_random_value(self, column):
        data_type = column.type
        print(f"\n\n data_type: {data_type} \n\n")
        column_name = column.name
        table_name = column.table.name

        def get_random_file_name(dir_path):
            file_names = os.listdir(dir_path)
            files_only = [entry for entry in file_names if os.path.isfile(os.path.join(dir_path, entry))]
            random_test_file_name = files_only[random.randint(0, len(files_only) - 1)]
            return random_test_file_name
        # for video storage
        if column_name in ["file_name"]:
            dir_path = "./db/assets"
            return get_random_file_name(dir_path)
        # for profile pics
        if column_name in ["profile_icon"]:
            dir_path = "./db/assets/images"
            return get_random_file_name(dir_path)
        
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
            # code fix should be somewhere around here
            return random_date(hardcoded_start_date, hardcoded_end_date)


    def init_table_data(self, list_of_table_rand):

        
        with Session(self.seed.engine) as session:
            # if i keep this cache object, I dont have to do
            # select queries assuming every record gets
            # correctly inserted
            # what should i do if this assumption fails?
            # TODO: answer above question

            # TODO: add try/except block to clean video_file_manager
            # if seeding errors out
            for table_state in list_of_table_rand:
                self.cache[table_state.name] = []
                table_instance = self.seed.get_table_metadata(table_state.name)

                for _ in range(table_state.num_records):
                    random_record = self.create_random_record(table_instance)
                    self.cache[table_state.name].append(random_record)
                    session.add(random_record)
                session.flush()
                #TODO: video id gets set after flush i believe
                # update video_file_manager
                # TODO?: may need to account for asynchronicity of flush
                """
                if table_state.name == "videos":
                    video_records = self.cache[table_state.name]
                    self.video_file_manager.load_videos(video_records)
                """
            session.commit()
        
        return
    

    
        
        # - and then create original ddl

        
