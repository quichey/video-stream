from sqlalchemy import create_engine
from sqlalchemy import insert, select
from sqlalchemy import Boolean, Integer, String, DateTime

from db.DB_SCHEMA import database_specs, metadata_obj, 

"""
In my experience working at CliniComp,
there are cases where you'd want to keep unchanged data
within some sort of cache,
so could add these specific use-cases here if necessary to
facilitate low latency user-experiences

what should be the separation of duties in terms of Cache 
and the api/video_stream.py files?
Should Cache do all the sqlalchemy function calls?
seems like it, to mitigate number of imports/confusion between
where to put code
If so, what exactly is the point of api/video_stream.py?
I think it makes sense to have that file handle the WGSI/Gateway/HTTP
protocol things
The api/video_stream.py stuff i think will help facilitate scaling up
the server-side code for adding in new server instances/DB instances
"""
class Cache():
    def __init__(self):
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
    

    def get_comments(self, page_number, page_size=50):
        offset = page_size * page_number # need to change this later to make up for initial page w/different size
        data = []
        with self.engine.connect() as conn:
            comments_table = self.metadata_obj.tables["comments"]
            users_table = self.metadata_obj.tables["users"]
            select_cols = [comments_table.c.comment, user_table.c.name]
            stmt = select(select_cols).select_from(
                comments_table.join(
                    user_table,
                    comments_table.c.user_id == user_table.c.id
            )).limit(page_size).offset(offset)

            records = conn.execute(stmt)
            for row in records:
                """
                val = {}
                #val[pk_col_name] = row[pk_col_name]
                val[pk_col_name] = row[0]
                values.append(val)
                """
                #TODO: fill-in logic of extracting data from sqlalchemy
        return data
