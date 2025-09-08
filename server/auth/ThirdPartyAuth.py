from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps
from typing import Optional, override
from typing import Literal

from sqlalchemy.orm import Session

from db.Schema.Models import User, ThirdPartyAuthUser, ThirdPartyAuthToken
from auth import Auth
from api.util.cookie import set_auth_cookie, expire_cookie
from api.util.request_data import extract_user_session_cookie

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


@dataclass
class Cred:
    provider_user_id: str = None
    email: Optional[str] = None
    access_token: str = None
    refresh_token: Optional[str] = None
    expires_at: Optional[str] = None
    metadata: Optional[str] = None


class ThirdPartyAuth(Auth, ABC):
    PROVIDER = None

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

    """
    Can i make this not an abstract-method?
    Can most 3rd party authorizors follow the same basic flow of the callback
    - If user exists in ThirdPartyAuth table, don't create new record
    """

    @abstractmethod
    def extract_authorizor_creds(self, request, response) -> Cred:
        pass

    # TODO: change to get_user? and return None if doesn't exist?
    # should everything be in one Session object? these should all be
    # wrapped up into one transaction
    def check_user_exists(self, request, response, creds: Cred) -> bool:
        record = self.map_creds_to_auth_record(creds)
        with Session(self.engine) as session:
            # TODO: use session.filter on PROVIDER and provider_user_id
            result = (
                session.query(ThirdPartyAuthUser)
                .filter_by(
                    provider_user_id=record.provider_user_id,
                    provider=self.PROVIDER,
                )
                .first()
            )
            if result:
                return True

        return None

    def handle_callback(self, request, response) -> User | Literal[False]:
        """Handle User 3rd party credentials"""
        creds = self.extract_authorizor_creds(request, response)
        user_exists = self.check_user_exists(request, response, creds)
        set_auth_cookie(response, creds.access_token)
        if user_exists:
            return self.login(request, response)
        else:
            return self.register(request, response)

    @override
    def authorize(self, request, response) -> bool:
        client_token = extract_user_session_cookie(request)
        with Session(self.engine) as session:
            # TODO: handle refresh
            result = (
                session.query(ThirdPartyAuthToken)
                .filter_by(
                    access_token=client_token,
                )
                .first()
            )
            if result:
                return True

        return None

    def needs_authorization(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Step 1: call child-specific authorization (expected to be defined in child)
            if hasattr(self, "authorize"):
                self.authorize()

            # Step 2: base-class predefined steps
            print("Base class step: logging or validation")

            # Step 3: run the original function
            return func(*args, **kwargs)

        return wrapper

    @override
    def register(self, request, response) -> User | Literal[False]:
        creds = self.extract_authorizor_creds(request, response)
        # TODO: create record in ThirdPartyAuthUser
        # also create record in User table
        # also create record in ThirdPartyAuthToken table
        user = self.create_user(creds)
        third_party_user_record = self.create_third_party_user_record(creds, user)
        self.initialize_auth_record(creds, third_party_user_record)
        return user

    def create_third_party_user_record(
        self, creds: Cred, user: User
    ) -> ThirdPartyAuthUser:
        record = ThirdPartyAuthUser(
            user_id=user.id,
            provider=self.PROVIDER,
            provider_user_id=creds.provider_user_id,
        )
        with Session(self.engine) as session:
            session.add(record)
            session.commit()
        return record

    def get_third_party_user_record(self, creds: Cred) -> ThirdPartyAuthUser | None:
        record = ThirdPartyAuthUser(
            provider=self.PROVIDER,
            provider_user_id=creds.provider_user_id,
        )
        with Session(self.engine) as session:
            # TODO: use session.filter on PROVIDER and provider_user_id
            result = (
                session.query(ThirdPartyAuthUser)
                .filter_by(
                    provider_user_id=record.provider_user_id,
                    provider=self.PROVIDER,
                )
                .first()
            )
            if result:
                return result

        return None

    @override
    def login(self, request, response) -> User | Literal[False]:
        creds = self.extract_authorizor_creds(request, response)
        third_party_user_record = self.get_third_party_user_record(creds)
        # TODO:
        # get record in ThirdPartyAuthUser belonging to cred
        # also get record in User belonging to cred
        # also create record in ThirdPartyAuthToken table
        self.initialize_auth_record(creds, third_party_user_record)
        user = self.get_user_info(third_party_user_record)
        return user

    @override
    @needs_authorization
    def logout(self, request, response):
        expire_cookie("auth_cookie", response)
        # TODO: remove auth_token?
        # should I have another table
        # I think separate linking table
        # from users.id to google_provider_id
        # and then thirdpartytokens table

        # TODO: remove record from ThirdPartyAuthToken
        pass

    def create_user(self, creds) -> User:
        user = User(
            name=creds.email,  # TODO: gen random name
            email=creds.email,
        )
        # also save to mysql db
        with Session(self.engine) as session:
            session.add(user)
            session.commit()

        return user

    def get_user_info(self, third_party_user_record: ThirdPartyAuthUser) -> User:
        with Session(self.engine) as session:
            user = session.get(User, third_party_user_record.user_id)
            if user:
                return user
        raise Exception(f"Unable to get user record: {third_party_user_record}")

    def map_creds_to_auth_record(
        self, creds: Cred, third_party_user_record: ThirdPartyAuthUser
    ) -> ThirdPartyAuthToken:
        record = ThirdPartyAuthToken(
            third_party_auth_user_id=third_party_user_record.id,
            access_token=creds.access_token,
            refresh_token=creds.refresh_token,
            metadata=creds.metadata,
        )
        return record

    def initialize_auth_record(
        self, creds: Cred, third_party_user_record: ThirdPartyAuthUser
    ) -> ThirdPartyAuthToken:
        record = self.map_creds_to_auth_record(creds, third_party_user_record)
        with Session(self.engine) as session:
            session.add(record)
            session.commit()
        return record
