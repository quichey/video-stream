from .DB_SCHEMA import Base, Users, Videos, Comments
class Schema():
    
    #TODO: there should be a way to do this w/out copying pasting strings
    ## look it up
    def get_record_factory(self, table_name):
        mapping = {
            "users": Users,
            "videos": Videos,
            "comments": Comments,
        }
        return mapping[table_name]