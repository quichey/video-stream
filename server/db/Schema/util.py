from .Models import User, Video, Comment



#TODO: there should be a way to do this w/out copying pasting strings
## look it up
def get_record_factory(self, table_name):
    mapping = {
        "users": User,
        "videos": Video,
        "comments": Comment,
    }
    return mapping[table_name]