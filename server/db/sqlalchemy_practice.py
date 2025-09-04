from sqlalchemy import create_engine
from sqlalchemy import text

from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

# create engine
def start_engine():
    dialect = "mysql"
    db_api = "mysqlconnector"

    user = "new_user"
    pw = "password"
    hostname = "localhost:3306"
    dbname = "video_stream"
    url = f"{user}:{pw}@{hostname}/{dbname}"

    engine = create_engine(f"{dialect}+{db_api}://{url}", echo=True)
    return engine


def connect_engine(engine):
    with engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        print(result.all())


def commit_changes():
    engine = start_engine()
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()


def fetch_rows():
    engine = start_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for row in result:
            print(f"x: {row.x}  y: {row.y}")


def bind_parameters():
    engine = start_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
        for row in result:
            print(f"x: {row.x}  y: {row.y}")


def bind_multi_parameters():
    engine = start_engine()
    # instead of .connect, I can do .begin and then forego the last .commit statement, iirc
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
        )
        conn.commit()


from sqlalchemy.orm import Session

def test_session():
    engine = start_engine()
    stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
    with Session(engine) as session:
        result = session.execute(stmt, {"y": 6})
        for row in result:
            print(f"x: {row.x}  y: {row.y}")


def test_session_update():
    engine = start_engine()
    with Session(engine) as session:
        result = session.execute(
            text("UPDATE some_table SET y=:y WHERE x=:x"),
            [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
        )
        session.commit()


from sqlalchemy import MetaData
metadata_obj = MetaData()

from sqlalchemy import Table, Column, Integer, String
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(100)),
)


def read_user_table_def():
    print(f"name: {user_table.c.name}")

    keys = user_table.c.keys()
    print(f"keys: {keys}")


from sqlalchemy import ForeignKey
address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(100), nullable=False),
)


# as of now -- this just creates the database and all tables
# implement functions to fill in test-data
def seed_db():
    engine = start_engine()
    metadata_obj.create_all(engine)

def inspect_address_table_fk():
    fks = address_table.foreign_key_constraints
    for fk in fks:
        print(f"Foreign Key: {fk.name}")

        # just need these following lines to get fk info
        for column in fk.columns:
            print(f"  Column: {column.name}")
        print(f"  References: {fk.referred_table.name}")


def inspect_address_table_pk():

    pk = address_table.primary_key
    pk_defs = []
    for column in pk.columns:
        print(f"column.name: {column.name}")
        pk_defs.append(column.name)

    return pk_defs

from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass

def print_base_metadata():
    print(f"Base.metadata: {Base.metadata}")

def print_base_registry():
    print(f"Base.registry: {Base.registry}")


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


def create_user():
    sandy = User(name="sandy", fullname="Sandy Cheeks")
    return sandy

def create_data():
    engine = start_engine()
    Base.metadata.create_all(engine)