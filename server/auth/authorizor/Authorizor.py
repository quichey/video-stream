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
        authorizor_passed = self.authorize(request, response)
        if not authorizor_passed:
            raise SecurityError(f"Authorizor failed: {self}")
        return self.AUTH_COOKIE.authenticate_cookies(request, response)

    def fetch_user_record(self, cookie) -> User | Literal[False]:
        cookie_record = self.AUTH_COOKIE.fetch_user_cookie_record(cookie)
        # also save to mysql db
        with Session(self.engine) as session:
            user_record = session.get(User, cookie_record.user_id)
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

    def handle_third_party_auth(self, request, response):
        pass
