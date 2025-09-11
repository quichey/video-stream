from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps
from typing import Optional
from typing import Literal
from typing_extensions import override

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from db.Schema.Models import User, ThirdPartyAuthUser, ThirdPartyAuthToken
from auth.auth import Auth
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


def needs_authorization(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Step 1: call child-specific authorization (expected to be defined in child)
        if hasattr(self, "authorize"):
            self.authorize(*args, **kwargs)

        # Step 2: base-class predefined steps
        print("Base class step: logging or validation")

        # Step 3: run the original function
        return func(self, *args, **kwargs)

    return wrapper


@dataclass
class Cred:
    provider_user_id: str = None
    email: Optional[str] = None
    access_token: str = None
    refresh_token: Optional[str] = None
    expires_at: Optional[str] = None
    auth_metadata: Optional[str] = None


class ThirdPartyAuth(Auth, ABC):
    PROVIDER = None

    @abstractmethod
    def get_authorize_url(self, redirect_uri: str) -> str:
        """Return URL to redirect user for login"""
        pass

    def get_cred_info(self, request, response) -> Cred:
        """Handle User 3rd party credentials"""
        creds = self._extract_authorizor_creds(request, response)
        return creds

    def handle_callback(self, request, response, creds: Cred) -> User | Literal[False]:
        """Handle User 3rd party credentials"""
        user_exists = self._check_user_exists(request, response, creds)
        if user_exists:
            user_record = self.login(request, response, creds)
        else:
            user_record = self.register(request, response, creds)
        set_auth_cookie(response, creds.access_token)
        print(f"\n\n handle_callback user_record: {user_record} \n\n")
        return user_record

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

    @override
    def register(self, request, response, creds: Cred) -> User | Literal[False]:
        # TODO: create record in ThirdPartyAuthUser
        # also create record in User table
        # also create record in ThirdPartyAuthToken table
        SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        with SessionLocal() as session:
            try:
                user = self._create_user(creds, session)
                third_party_user_record = self._create_third_party_user_record(
                    creds, user, session
                )
                self._initialize_auth_record(creds, third_party_user_record, session)
                session.commit()
                return user
            except Exception as e:
                session.rollback()
                raise e

    @override
    def login(self, request, response, creds: Cred) -> User | Literal[False]:
        third_party_user_record = self._get_third_party_user_record(creds)
        # TODO:
        # get record in ThirdPartyAuthUser belonging to cred
        # also get record in User belonging to cred
        # also create record in ThirdPartyAuthToken table
        with Session(self.engine) as session:
            self._initialize_auth_record(creds, third_party_user_record, session)
            session.commit()
        user = self._get_user_info(third_party_user_record)
        return user

    @override
    @needs_authorization
    def logout(self, request, response) -> bool:
        # TODO: remove auth_token?
        # should I have another table
        # I think separate linking table
        # from users.id to google_provider_id
        # and then thirdpartytokens table

        # TODO: remove record from ThirdPartyAuthToken
        with Session(self.engine) as session:
            access_token = extract_user_session_cookie(request)
            record = (
                session.query(ThirdPartyAuthToken)
                .filter_by(access_token=access_token)
                .first()
            )
            deleted_record = session.delete(record)
            if deleted_record:
                expire_cookie("auth_cookie", response)
                return True
        return False

    @property
    def oauth_client(self):
        return self._oauth_client

    @oauth_client.setter
    def oauth_client(self, new_value):
        self._oauth_client = new_value

    """
    Can i make this not an abstract-method?
    Can most 3rd party authorizors follow the same basic flow of the callback
    - If user exists in ThirdPartyAuth table, don't create new record
    """

    @abstractmethod
    def _extract_authorizor_creds(self, request, response) -> Cred:
        pass

    # TODO: change to get_user? and return None if doesn't exist?
    # should everything be in one Session object? these should all be
    # wrapped up into one transaction
    def _check_user_exists(self, request, response, creds: Cred) -> bool:
        with Session(self.engine) as session:
            # TODO: use session.filter on PROVIDER and provider_user_id
            result = (
                session.query(ThirdPartyAuthUser)
                .filter_by(
                    provider_user_id=creds.provider_user_id,
                    provider=self.PROVIDER,
                )
                .first()
            )
            if result:
                return True

        return None

    def _create_third_party_user_record(
        self, creds: Cred, user: User, session: Session
    ) -> ThirdPartyAuthUser:
        record = ThirdPartyAuthUser(
            user_id=user.id,
            provider=self.PROVIDER,
            provider_user_id=creds.provider_user_id,
        )
        session.add(record)
        session.flush()
        return record

    def _get_third_party_user_record(self, creds: Cred) -> ThirdPartyAuthUser | None:
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

    def _create_user(self, creds, session: Session) -> User:
        user = User(
            name=creds.email,  # TODO: gen random name
            email=creds.email,
        )
        # also save to mysql db
        session.add(user)
        session.flush()
        return user

    def _get_user_info(self, third_party_user_record: ThirdPartyAuthUser) -> User:
        with Session(self.engine) as session:
            user = session.get(User, third_party_user_record.user_id)
            if user:
                return user
        raise Exception(f"Unable to get user record: {third_party_user_record}")

    def _map_creds_to_auth_record(
        self, creds: Cred, third_party_user_record: ThirdPartyAuthUser
    ) -> ThirdPartyAuthToken:
        record = ThirdPartyAuthToken(
            third_party_auth_user_id=third_party_user_record.id,
            access_token=creds.access_token,
            refresh_token=creds.refresh_token,
            auth_metadata=creds.auth_metadata,
        )
        return record

    def _initialize_auth_record(
        self, creds: Cred, third_party_user_record: ThirdPartyAuthUser, session: Session
    ) -> ThirdPartyAuthToken:
        record = self._map_creds_to_auth_record(creds, third_party_user_record)
        session.add(record)
        return record
