import os
import datetime

from sqlalchemy import (
    JSON,
    MetaData,
    Table,
    Column,
    Boolean,
    Integer,
    String,
    DateTime,
    ForeignKey,
    VARBINARY,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import DeclarativeBase

from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from util.env import load_server_env, load_providers_env


class Base(DeclarativeBase):
    pass


metadata_obj = MetaData()

load_server_env()
load_providers_env()

admin_specs = {
    "dialect": "mysql",
    "db_api": "mysqlconnector",
    "user": "root",
    "pw": os.getenv("MYSQL_ADMIN_SECRET"),
    "hostname": "localhost:3306",
}

database_specs = {
    "dialect": "mysql",
    "db_api": "mysqlconnector",
    "user": "new_user",
    "pw": "password",
    "hostname": "localhost:3306",
    "dbname": "video_stream",
}

"""
create _specs but for azure-cloud sql
"""
admin_specs_cloud_sql = {
    "dialect": "mysql",
    "db_api": "mysqlconnector",
    "user": os.getenv("MYSQL_ADMIN_NAME"),
    "pw": os.getenv("MYSQL_ADMIN_PW"),
    "hostname": f"{os.getenv('MYSQL_DB_NAME')}.mysql.database.azure.com",
    "provider": "azure",
}

# TODO: make non-admin mysql user on azure
database_specs_cloud_sql = {
    "dialect": "mysql",
    "db_api": "mysqlconnector",
    "user": os.getenv("MYSQL_ADMIN_NAME"),
    "pw": os.getenv("MYSQL_ADMIN_PW"),
    "hostname": f"{os.getenv('MYSQL_DB_NAME')}.mysql.database.azure.com",
    "dbname": "video_stream",
    "provider": "azure",
    # "CLOUD_SQL_CONNECTION_NAME": "copy-youtube-461223:us-central1:mysql-db"
}

"""
create _specs but for g-cloud sql
"""
# admin_specs_cloud_sql = {
#    "dialect": "mysql",
#    "db_api": "mysqlconnector",
#    "user": "mysql-db-on-g-cloud-sql",
#    "pw": os.getenv("MYSQL_ADMIN_SECRET"),
#    "hostname": "35.226.88.211:3306"
# }

# database_specs_cloud_sql = {
#    "dialect": "mysql",
#    "db_api": "mysqlconnector",
#    "user": "mysql-db-on-g-cloud-sql",
#    "pw": os.getenv("MYSQL_ADMIN_SECRET"),
#    "hostname": "35.226.88.211:3306",
#    "dbname": "video_stream",
#    "CLOUD_SQL_CONNECTION_NAME": "copy-youtube-461223:us-central1:mysql-db"
# }

users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("email", String(30)),
)

videos_table = Table(
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
    # Column("thread_comment_id", ForeignKey("comments.id"), nullable=True),
    Column("thread_comment_id", Integer),
    Column("comment", String(100)),
    Column("date", DateTime),
    Column("edited_flag", Boolean),
)

comment_likes_table = Table(
    "comment_likes",
    metadata_obj,
    # Column("id", Integer, primary_key=True),
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
    name: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[Optional[str]] = mapped_column(String(30))
    profile_icon: Mapped[Optional[str]] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(VARBINARY(255))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r}, password={self.password!r})"


class UserCookie(Base):
    __tablename__ = "user_cookies"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    cookie: Mapped[str] = mapped_column(String(100), unique=True)

    def __repr__(self) -> str:
        return f"UserCookie(id={self.id!r}, user_id={self.user_id!r}, cookie={self.cookie!r})"


class ThirdPartyAuthUser(Base):
    __tablename__ = "third_party_auth_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    provider: Mapped[str] = mapped_column(String(50))
    provider_user_id: Mapped[str] = mapped_column(String(255))

    user = relationship(
        "User", back_populates="third_party_accounts"
    )  # TODO: what is this?

    __table_args__ = (
        # Enforce uniqueness of provider + provider_user_id
        UniqueConstraint("provider", "provider_user_id", name="uq_provider_user"),
        # Add indexes for common lookups
        Index("idx_user_id", "user_id"),
        Index("idx_provider", "provider"),
    )


class ThirdPartyAuthToken(Base):
    __tablename__ = "third_party_auth_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    third_party_auth_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("third_party_auth_users.id")
    )
    access_token: Mapped[str] = mapped_column(String(500))
    refresh_token: Mapped[Optional[str]] = mapped_column(String(500))
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)  # type: ignore
    metadata: Mapped[dict] = mapped_column(JSON)

    user = relationship(
        "User", back_populates="third_party_accounts"
    )  # TODO: what is this?


class Video(Base):
    __tablename__ = "videos"
    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String(30))
    file_dir: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    date_updated: Mapped[str] = mapped_column(DateTime)
    date_created: Mapped[str] = mapped_column(DateTime)

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
