from typing import Optional, Union, Literal
from sqlalchemy.orm import Session

from auth.native.native import NATIVE_AUTH, NativeAuth
from auth.ThirdPartyAuth import ThirdPartyAuth
from auth.google_auth.google_auth import GOOGLE_AUTH

from api.util.error_handling import SecurityError
from db.Schema.Models import User
from api.util.db_engine import DataBaseEngine
from auth.authorizor.auth_cookie import AuthCookie
from db.Schema.Models import UserCookie

from api.util.request_data import (
    extract_user_session_cookie,
)


class Authorizor(DataBaseEngine):
    AUTH_COOKIE: AuthCookie = None  # TODO: does this belong in Auth class?
    AUTH_INSTANCE: Optional[Union[NativeAuth, ThirdPartyAuth]] = None

    def __init__(
        self, auth_type: Optional[Union[NativeAuth, ThirdPartyAuth]] = NativeAuth
    ):
        if auth_type == NativeAuth:
            self.AUTH_INSTANCE = NATIVE_AUTH
        elif auth_type == ThirdPartyAuth:
            self.AUTH_INSTANCE = None

    def restore_lost_session(self, request, response):
        user_cookie = extract_user_session_cookie(request)
        return self.fetch_user_record(user_cookie)

    def authenticate(self, request, response) -> Literal[True]:
        # TODO: Think i want to merge the user_cookies table with third_party_auths table to
        # make the schema cleaner
        # OR just attach new cookie value within ThirdPartyAuthorizors
        if self.AUTH_INSTANCE == NATIVE_AUTH:
            return self.AUTH_COOKIE.authenticate_cookies(request, response)
        elif self.AUTH_INSTANCE == ThirdPartyAuth:
            return self.AUTH_INSTANCE.authorize(request, response)

    def pre_authenticate_session(self, request, response) -> Literal[True]:
        authorizor_passed = self.authorize(request, response)
        if not authorizor_passed:
            raise SecurityError(f"Authorizor failed: {self}")
        return self.AUTH_COOKIE.authenticate_cookies(request, response)

    def fetch_user_cookie_record(self, cookie) -> UserCookie | Literal[False]:
        # also save to mysql db
        with Session(self.engine) as session:
            cookie_record = session.query(UserCookie).filter_by(cookie=cookie).first()
            return cookie_record

        return False

    def fetch_user_record(self, cookie) -> User | Literal[False]:
        # TODO: classmethod on AUTH_COOKIE?
        cookie_record = self.fetch_user_cookie_record(cookie)
        # also save to mysql db
        with Session(self.engine) as session:
            user_record = session.get(User, cookie_record.user_id)
            self.AUTH_COOKIE = AuthCookie(user_record)
            return user_record

        return False

    def handle_login(self, request, response):
        user_instance = self.AUTH_INSTANCE.login()
        self.AUTH_COOKIE = AuthCookie(user_instance)
        return user_instance

    def handle_logout(self, request, response) -> Literal[True]:
        # self.NATIVE_AUTH.logout(request, response)
        if not self.authenticate(request, response):
            # Invalid credentials
            response.status_code = 401
            raise SecurityError(f"Authorizor failed: {self}")

        self.AUTH_COOKIE.clear_cookie(request, response)
        return True

    def handle_register(self, request, response):
        user_instance = self.AUTH_INSTANCE.register()
        self.AUTH_COOKIE = AuthCookie(user_instance)
        return user_instance

    def handle_third_party_auth(self, request, response) -> User | Literal[False]:
        url_route = request.path
        if url_route == "/auth/google/callback":
            self.AUTH_INSTANCE = GOOGLE_AUTH
        user_instance = self.AUTH_INSTANCE.handle_callback(request, response)
        return user_instance
