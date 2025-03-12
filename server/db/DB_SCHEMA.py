from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey

metadata_obj = MetaData()

database_specs = {
    "dialect": "mysql",
    "db_api": "mysqlconnector",
    "user": "new_user",
    "pw": "password",
    "hostname": "localhost:3306",
    "dbname": "video_stream"
}


users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
)

comments_table = Table(
    "comments",
    metadata_obj,
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("comment", String(100)),
)