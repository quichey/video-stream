database_name = "video_stream"

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