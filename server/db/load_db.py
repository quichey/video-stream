# may expand this file to be named snapshot_db
# to draw inspiration from ISS/Clinicomp as well as the
# glorious game Pokemon Snap
# -- ideally i would make functionality to
# - Check if database named video_stream exists
# - - if not, create it with a test user
# - create/load tables with demo-able data
# - prepare indices for optimal searching/fetching for appropriate cases

def create_table(table_name: str, columns: list):
    # columns is nested list depth 2
    # second depth is 2-tuple of (column_name, data_type)
    pass

def create_random_value(data_type):
    # do case switch on data_type
    pass

def create_random_record(table):
    # get table specs for table object
    # get column names and column types
    # use create_random_value
    # sqlalchemy may have function available to do this
    pass
