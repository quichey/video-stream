from sqlalchemy.orm import Session
from typing import Literal

from api.util.error_handling import SecurityError
from db.Schema.Models import User, UserCookie
from api.util.db_engine import DataBaseEngine
from api.util.cookie import generate_cookie, expire_cookie
from api.util.request_data import (
    extract_user_session_cookie,
    has_user_session_cookie,
)


class AuthCookie(DataBaseEngine):
    COOKIE_RECORD_ID = None  # TODO: does this belong in Auth class?
    COOKIE_VALUE = None
    USER_INSTANCE: User = None

    def __init__(self, user_instance: User, request, response):
        self.USER_INSTANCE = user_instance
        self.generate_auth_cookie(request, response)

    def store_cookie_record(self) -> UserCookie | Literal[False]:
        # also save to mysql db
        with Session(self.engine) as session:
            cookie_record = UserCookie(
                user_id=self.USER_INSTANCE.id,
                cookie=self.COOKIE_VALUE,
            )
            session.add(cookie_record)
            session.commit()
            if cookie_record.id is not None:
                self.COOKIE_RECORD_ID = cookie_record.id
                return cookie_record

        return False

    def delete_cookie_record(self) -> bool:
        with Session(self.engine) as session:
            rows_deleted = (
                session.query(UserCookie)
                .filter(UserCookie.id == self.COOKIE_RECORD_ID)
                .delete()
            )
            session.commit()

            if rows_deleted > 0:
                return True
            else:
                rows_deleted = (
                    session.query(UserCookie)
                    .filter(UserCookie.cookie == self.COOKIE_VALUE)
                    .delete()
                )
                session.commit()
                if rows_deleted > 0:
                    return True
                else:
                    return False
        return False

    def authenticate_cookies(self, request, response) -> Literal[True]:
        if not has_user_session_cookie(request):
            raise SecurityError("No User Session Cookie")
        cookie = extract_user_session_cookie(request)
        if cookie != self.COOKIE_VALUE:
            raise SecurityError("Auth Cookie does not Match")
        return True

    def generate_auth_cookie(self, request, response):
        self.COOKIE_VALUE = generate_cookie("auth_cookie", response)
        self.store_cookie_record()
        return self.COOKIE_VALUE

    def clear_cookie(self, request, response):
        expire_cookie("auth_cookie", response)
        self.delete_cookie_record()
        self.COOKIE_VALUE = None
