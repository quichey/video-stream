from dataclasses import dataclass
from typing import Literal
from sqlalchemy.orm import Session
from typing import Optional
from api.util.cookie import generate_cookie

from api.orchestrator.session.AnonymousSession import AnonymousSession
from api.orchestrator.session.UserSession import UserSession
from api.util.request_data import (
    has_user_session_cookie,
    extract_user_session_cookie,
)

from db.Schema.Models import User, UserCookie
from api.util.db_engine import DataBaseEngine
from auth.native.native import NATIVE_AUTH, NativeAuth


@dataclass
class SessionPair(DataBaseEngine):
    anonymous_session: AnonymousSession
    user_session: Optional[UserSession] = None
    LONG_TERM_COOKIE_ID: Optional[str] = None
    NATIVE_AUTH: Optional[NativeAuth] = NATIVE_AUTH

    def create_cookie(self, request, response):
        return self.generate_long_term_cookie(request, response)

    def generate_long_term_cookie(self, request, response):
        self.LONG_TERM_COOKIE_ID = generate_cookie("long_term_session", response)
        return self.LONG_TERM_COOKIE_ID

    def create_user_session(self, request, response):
        self.user_session = UserSession(request, response)
        return self.user_session

    def restore_lost_user_session(self, request, response) -> UserSession:
        has_user_cookie = has_user_session_cookie(request)
        if has_user_cookie:
            # TODO: what if user_session is empty? create user_session
            # need to return session_token, i think already handled
            # TODO: return user's info on /load-session api
            # ----- name, profile pic info
            if not self.user_session:
                print("\n\n got here: if not session_pair.user_session \n\n")
                user_cookie = extract_user_session_cookie(request)
                user_record = self.fetch_user_record(user_cookie)
                self.user_session = UserSession(
                    user_cookie,
                    user_record,
                    self.NATIVE_AUTH,
                    request,
                    response,
                )

            return self.user_session

    def fetch_user_record(self, cookie) -> User | Literal[False]:
        cookie_record = self.fetch_user_cookie_record(cookie)
        # also save to mysql db
        with Session(self.engine) as session:
            user_record = session.get(User, cookie_record.user_id)
            return user_record

        return False

    def fetch_user_cookie_record(self, cookie) -> UserCookie | Literal[False]:
        # also save to mysql db
        with Session(self.engine) as session:
            cookie_record = session.query(UserCookie).filter_by(cookie=cookie).first()
            return cookie_record

        return False
