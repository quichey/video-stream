from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

from db.Schema import database_specs, database_specs_cloud_sql, Base, User

"""
What is a reasonalbe Interface for this base class?
User flow is that they can either:
- Register and account -- return user_info?
- login -- return user_info?
- logout -- return 'success' or 'fail'?

Should I handle personal Database stuff here?
But also have the Cache.SessionManager class.

But Having separate tables seems like enough encapsulation
to keep the DB things separate between the two modules?

Already have users table
Would a Login table be good?

Cache.SessionManager already needs to keep track of states
for essentially all user state (comments, video, etc)
Rather leave all User database updates and reads to here
"""
class Auth(ABC):
    def __init__(self, deployment="local"):
        if deployment == "local":
            self.database_specs = database_specs
        elif deployment == "cloud":
            self.database_specs = database_specs_cloud_sql
        # temporary hotfix based off reading cloud run error logs
        else:
            self.database_specs = database_specs_cloud_sql
        self.deployment = deployment
        print(f"\n\n self.database_specs: {self.database_specs} \n\n")
        self.metadata_obj = Base.metadata
        self.construct_engine(self.database_specs)

    @abstractmethod
    def register(self, user_info):
        pass
    @abstractmethod
    def login(self, user_info):
        pass
    @abstractmethod
    def logout(self, user_info):
        pass
    
    def create_user(self, user_info) -> User:
        user = User(
            name=user_info.name,
            email=user_info.email,
        )
        # also save to mysql db
        with Session(self.engine) as session:
            session.add(user)
            session.commit()

        return user

    def get_user_info(self, user_id) -> User:
        with Session(self.engine) as session:
            user = session.get(User, user_id)
        return user
    
    def construct_engine(self, database_specs):
        if self.deployment == "local": 
            dialect = database_specs["dialect"]
            db_api = database_specs["db_api"]

            user = database_specs["user"]
            pw = database_specs["pw"]
            hostname = database_specs["hostname"]
            dbname = database_specs["dbname"]
            url = f"{user}:{pw}@{hostname}/{dbname}"

            engine = create_engine(f"{dialect}+{db_api}://{url}", echo=True)
        elif database_specs["provider"] == "azure":
            dialect = database_specs["dialect"]
            db_api = database_specs["db_api"]

            user = database_specs["user"]
            pw = database_specs["pw"]
            hostname = database_specs["hostname"]
            dbname = database_specs["dbname"]
            url = f"{user}:{pw}@{hostname}/{dbname}"

            engine = create_engine(f"{dialect}+{db_api}://{url}", echo=True)

        #Google cloud run deployment
        else:
            DB_USER = database_specs["user"]
            DB_PASS = database_specs["pw"]
            DB_NAME = database_specs["dbname"]
            CLOUD_SQL_CONNECTION_NAME = database_specs["CLOUD_SQL_CONNECTION_NAME"]

            # Unix socket path (Cloud Run mounts /cloudsql)
            unix_socket_path = f"/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"

            # SQLAlchemy connection URL (note: use pymysql)
            DATABASE_URI = (
                f"mysql+pymysql://{DB_USER}:{DB_PASS}@/{DB_NAME}"
                f"?unix_socket={unix_socket_path}"
            )

            engine = create_engine(DATABASE_URI, pool_pre_ping=True)
        self.engine = engine
        return engine