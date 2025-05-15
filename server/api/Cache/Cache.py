from sqlalchemy import create_engine
from sqlalchemy import select

from db.Schema import database_specs, Base
#from api.Cache.SessionManagement import SessionManagement
from .SessionManagement import SessionManagement

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


This class is where we can store session data not in the Databases
some kind of token/cookie to preserve the state of a user's scrolling through 
comments session
"""
class Cache():

    def __init__(self):
        self.database_specs = database_specs
        self.metadata_obj = Base.metadata
        self.construct_engine(database_specs)
        self.session_manager = SessionManagement()
    
    
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


    def get_session(self, user_info, existing_session_info):
        # extract user identity from request object
        # generate a session token here or on client?
        # i think here, then send it to the client for them to store in
        # the javascript

        session_info = self.session_manager.register_user(user_info, existing_session_info)
        return session_info
    

    """
    * From google search -- Performance optimization for later
    Performance Considerations:
        While the order of LIMIT and OFFSET doesn't directly impact performance in most cases,
        using large OFFSET values can lead to slower queries, especially on large tables,
        as the database needs to scan through a large number of rows before applying the LIMIT. 
    """
    def get_comments(self, session_info, page_number=0, page_size=50):
        limit = page_size
        offset = page_size * page_number # need to change this later to make up for initial page w/different size

        if session_info is not None:
            current_state_of_comments = self.session_manager.get_state(session_info, "comments")
            offset = current_state_of_comments["offset"]
            limit = current_state_of_comments["limit"]
            print(f"\n\n offset: {offset} \n\n")
            print(f"\n\n limit: {limit} \n\n")

        data = []
        with self.engine.connect() as conn:
            comments_table = self.metadata_obj.tables["comments"]
            users_table = self.metadata_obj.tables["users"]
            select_cols = [comments_table.c.comment, users_table.c.name]
            stmt = select(
                *select_cols
            ).select_from(
                comments_table
            ).join(
                    users_table,
                    comments_table.c.user_id == users_table.c.id
            ).limit(
                limit
            ).offset(
                offset
            )

            records = conn.execute(stmt)
            new_offset = offset
            for row in records:
                new_offset = new_offset + 1

                comment_data_point = {
                    "comment": row[0],
                    "user_name": row[1]
                }
                data.append(comment_data_point)

            self.session_manager.update_state(session_info, "comments", "offset", new_offset)

        return data

    """
    Should I have session_info here if i intend this for admin stuff?
    I would need something like this possibly for refreshing the page
    or something
    """
    def clear_user_session(self, user_id, session_info):
        self.session_manager.exit_session(user_id, session_info)
        # add some security measures so that 
        # a random person can't randomly ruin another
        # person's session

        # have SessionManagement clear self.current_state of user_id/token info
        return


    """
    Should I have session_info here if i intend this for admin stuff?
    I would need something like this possibly for refreshing the page
    or something
    """
    def clear_user_session_admin(self, user_id):
        self.session_manager.exit_session_admin(user_id)
        # add some security measures so that 
        # a random person can't randomly ruin another
        # person's session

        # have SessionManagement clear self.current_state of user_id/token info
        return