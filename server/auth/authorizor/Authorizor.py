from typing import Optional, Union, Literal
from sqlalchemy.orm import Session

from auth.native.native import NATIVE_AUTH, NativeAuth
from auth.google_auth.google_auth import GOOGLE_AUTH, GoogleAuth

from api.util.error_handling import SecurityError
from db.Schema.Models import User
from api.util.db_engine import DataBaseEngine
from auth.authorizor.auth_cookie import AuthCookie


class Authorizor(DataBaseEngine):
    AUTH_COOKIE: AuthCookie = None  # TODO: does this belong in Auth class?
    AUTH_INSTANCE: Optional[Union[NativeAuth, GoogleAuth]] = None

    def __init__(self, auth_type: Optional[Union[NativeAuth, GoogleAuth]] = NativeAuth):
        if auth_type == NativeAuth:
            self.AUTH_INSTANCE = NATIVE_AUTH
        elif auth_type == GoogleAuth:
            self.AUTH_INSTANCE = GOOGLE_AUTH

    def authenticate(self, request, response) -> Literal[True]:
        return self.AUTH_COOKIE.authenticate_cookies(request, response)

    def pre_authenticate_session(self, request, response) -> Literal[True]:
        authorizor_passed = self.AUTHORIZOR.authorize(request, response)
        if not authorizor_passed:
            raise SecurityError(f"Authorizor failed: {self.AUTHORIZOR}")
        return self.authenticate_cookies(request, response)

    def fetch_user_record(self, cookie) -> User | Literal[False]:
        cookie_record = self.AUTH_COOKIE.fetch_user_cookie_record(cookie)
        # also save to mysql db
        with Session(self.engine) as session:
            user_record = session.get(User, cookie_record.user_id)
            return user_record

        return False

    def handle_login(self, request, response):
        return self.AUTH_INSTANCE.login()

    def handle_logout(self, request, response):
        return self.AUTH_INSTANCE.logout()

    def handle_register(self, request, response):
        return self.AUTH_INSTANCE.register()

    def handle_third_party_auth(self, request, response):
        pass
