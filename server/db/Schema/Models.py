import os
from dotenv import load_dotenv

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Boolean, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase

from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

metadata_obj = MetaData()

load_dotenv()
admin_specs = {
    "dialect": "mysql",
    "db_api": "mysqlconnector",
    "user": "root",
    "pw": os.getenv("MYSQL_ADMIN_SECRET"),
    "hostname": "localhost:3306",
    "dbname": "video_stream"
}

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

videos_table= Table(
    "videos",
    metadata_obj,
    Column("id", Integer, primary_key=True),

    Column("file", String(100)),
    Column("user_id", ForeignKey("users.id"), nullable=False),

)

comments_table = Table(
    "comments",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("video_id", ForeignKey("videos.id"), nullable=False),
    #Column("thread_comment_id", ForeignKey("comments.id"), nullable=True),
    Column("thread_comment_id", Integer),

    Column("comment", String(100)),
    Column("date", DateTime),
    Column("edited_flag", Boolean),
)

comment_likes_table = Table(
    "comment_likes",
    metadata_obj,
    #Column("id", Integer, primary_key=True),
    # not yet certain if this is the proper way to define multi-column primary key
    # i'll check later or something
    # need this to ensure there is no weird duplication of records with
    # different "id"s but the same comment_id and same user_id
    # this wouldn't make sense
    Column("comment_id", ForeignKey("comments.id"), nullable=False, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False, primary_key=True),

    Column("like_dislike_flag", Boolean),
)



class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"


class Video(Base):
    __tablename__ = "videos"
    id: Mapped[int] = mapped_column(primary_key=True)
    file: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"Video(id={self.id!r}, file={self.file!r}, user_id={self.user_id!r})"


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    video_id: Mapped[int] = mapped_column(Integer, ForeignKey("videos.id"))

    def __repr__(self) -> str:
        return f"Comment(id={self.id!r}, comment={self.comment!r}, user_id={self.user_id!r})"