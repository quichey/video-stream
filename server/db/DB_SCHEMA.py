from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Boolean, Integer, String
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
    Column("email", String(30)),
)

comments_table = Table(
    "comments",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("thread_comment_id", ForeignKey("comments.id"), nullable=True),

    Column("comment", String(100)),
    Column("date", String(30)),
    Column("edited_flag", Boolean),
)

comment_likes_table = Table(
    "comment_likes",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("comment_id", ForeignKey("comments.id"), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),

    Column("like_dislike_flag", Boolean),
)