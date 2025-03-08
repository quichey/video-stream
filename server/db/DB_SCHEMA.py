database_specs = {
    "dialect": "mysql",
    "db_api": "mysqlconnector",
    "user": "new_user",
    "pw": "password",
    "hostname": "localhost:3306",
    "dbname": "video_stream"
}

class Table():
    pass


class Comments(Table):
    comment = str
    user_id = int
    pass


class Users(Table):
    id = int
    name = str
    pass