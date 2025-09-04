from abc import ABC, abstractmethod
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

from db.Schema import database_specs, database_specs_cloud_sql, Base, User
from auth import Auth

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
class Auth(Auth, ABC):
    def __init__(self, deployment, *args, **kwargs):
        super().__init__(deployment, args, **kwargs)
    
    @property
    def oauth_client(self):
        return self._oauth_client
    
    @oauth_client.setter
    def oauth_client(self, new_value):
        self._oauth_client = new_value

    @abstractmethod
    def get_authorize_url(self, redirect_uri: str) -> str:
        """Return URL to redirect user for login"""
        pass

    def needs_authorization(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Step 1: call child-specific authorization (expected to be defined in child)
            if hasattr(self, 'authorize'):
                self.authorize()

            # Step 2: base-class predefined steps
            print("Base class step: logging or validation")

            # Step 3: run the original function
            return func(*args, **kwargs)
        return wrapper

    @abstractmethod
    def authorize(self, user_info):
        pass

    @needs_authorization
    def register(self, user_info) -> User:
        user = self.create_user(user_info=user_info)

        return user

    @needs_authorization
    def login(self, user_info) -> User:
        user = self.get_user_info(user_info["id"])
        return user

    @needs_authorization
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
