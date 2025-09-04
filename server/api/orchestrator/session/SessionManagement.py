from dataclasses import dataclass
from typing import Optional
from typing import Literal
from sqlalchemy.orm import Session

from api.orchestrator.session.Session import SessionBase
from api.orchestrator.session.AnonymousSession import AnonymousSession
from api.orchestrator.session.UserSession import UserSession
from api.util.request_data import (
    has_user_info,
    extract_long_term_cookie,
    has_user_session_cookie,
    extract_user_session_cookie,
    attach_data_to_payload,
)
from api.util.cookie import generate_cookie
from auth.native.native import NativeAuth
from db.Schema.Models import User, UserCookie
from api.util.db_engine import DataBaseEngine

class SecurityError(Exception):
    pass

@dataclass
class SessionPair:
    anonymous_session: AnonymousSession
    user_session: Optional[UserSession] = None
    LONG_TERM_COOKIE_ID: Optional[str] = None

    def create_cookie(self, request, response, deployment):
        self.DEPLOYMENT = deployment
        return self.generate_long_term_cookie(request, response)

    def generate_long_term_cookie(self, request, response):
        self.LONG_TERM_COOKIE_ID = generate_cookie("long_term_session", self.DEPLOYMENT, response)
        return self.LONG_TERM_COOKIE_ID

    def create_user_session(self, request, response, deployment, storage):
        self.user_session = UserSession(request, response, deployment, storage)
        return self.user_session

 
@dataclass
class SessionRegistry:
    # str should be LONG_TERM_COOKIE_ID
    sessions: dict[str, SessionPair]

class SessionManagement(DataBaseEngine):
    SESSION_REGISTRY = None
    DEPLOYMENT = None
    STORAGE = None
    NATIVE_AUTH = None

    def __init__(self, deployment, storage):
        DataBaseEngine.__init__(self, deployment)
        self.DEPLOYMENT = deployment
        self.STORAGE = storage
        self.NATIVE_AUTH = NativeAuth(self.DEPLOYMENT)
        self.SESSION_REGISTRY = SessionRegistry(sessions={})
    
    def add_session(self, request, response):
        new_session = AnonymousSession(request, response, self.DEPLOYMENT, self.STORAGE)
        print(f"\n\n new_session: {new_session} \n\n")
        session_pair = SessionPair(
            anonymous_session=new_session
        )
        session_uuid = session_pair.create_cookie(request, response, self.DEPLOYMENT)
        self.SESSION_REGISTRY.sessions[session_uuid] = session_pair
        #TODO: add check for user's auth cookie
        # COOKIE does not have info that can translate to user-id
        #TODO: add auth cookies to DB?
        print(f"\n\n new_session: {new_session} \n\n")
        has_user_cookie = has_user_session_cookie(request)
        if has_user_cookie:
            return self.restore_lost_user_session(session_pair, request, response)
        else:
            return new_session

    def end_session(self, request):
        pass

    def get_session_pair(self, request) -> SessionPair:
        long_term_cookie_id = extract_long_term_cookie(request)
        #print(f"\n\n self.SESSIONS: {self.SESSIONS}")
        session_pair = self.SESSION_REGISTRY.sessions.get(long_term_cookie_id)
        return session_pair
    
    def fetch_user_cookie_record(self, cookie) -> UserCookie | Literal[False]:
        # also save to mysql db
        with Session(self.engine) as session:
            cookie_record = session.query(UserCookie).filter_by(cookie=cookie).first()
            return cookie_record
        
        return False

    def fetch_user_record(self, cookie) -> User | Literal[False]:
        cookie_record = self.fetch_user_cookie_record(cookie)
        # also save to mysql db
        with Session(self.engine) as session:
            user_record = session.get(User, cookie_record.user_id)
            return user_record
        
        return False


    def restore_lost_user_session(self, session_pair, request, response) -> UserSession:
        has_user_cookie = has_user_session_cookie(request)
        if has_user_cookie:
            #TODO: what if user_session is empty? create user_session
            # need to return session_token, i think already handled
            # TODO: return user's info on /load-session api
            # ----- name, profile pic info
            if not session_pair.user_session:
                print("\n\n got here: if not session_pair.user_session \n\n")
                user_cookie = extract_user_session_cookie(request)
                user_record = self.fetch_user_record(user_cookie)
                session_pair.user_session = UserSession(
                    user_cookie,
                    user_record,
                    self.NATIVE_AUTH,
                    request,
                    response,
                    self.DEPLOYMENT,
                    self.STORAGE
                )

            return session_pair.user_session

    def get_session(self, request, response) -> SessionBase:
        session_pair = self.get_session_pair(request)
        has_user_cookie = has_user_session_cookie(request)
        if has_user_cookie:
            return self.restore_lost_user_session(session_pair, request, response)
        else:
            return session_pair.anonymous_session
    
    def needs_restore_lost_session(self, request):
        long_term_cookie_id = extract_long_term_cookie(request)
        return long_term_cookie_id not in self.SESSION_REGISTRY.sessions.keys()

    def needs_new_session(self, request):
        no_long_term_cookie = not extract_long_term_cookie(request)
        print(f"\n\n request.cookies.get: {extract_long_term_cookie(request)}")
        print(f"\n\n no_long_term_cookie: {no_long_term_cookie}")
        no_user_info = not has_user_info(request)
        # TODO: is checking no_user_info important?
        return no_long_term_cookie and no_user_info
    
    def on_request(self, request, response):
        # check the request for existing cookie
        # if no cookie present, and no User Id passed in, then...
        # generate a new Session Object and generate cookies
        # Otherwise, if cookie present and no User Id passed in...
        # just get the data
        # If cookie present and User Id is passed in, authenticate user and cookies?

        # 4 cases:
        # 1. No cookies and no User Info passed
        # 2. Cookies and no User Info passed
        # 3. Cookies and User Info passed in
        # 4. No Cookie and User Info passed

        # ideally want all User Info things to go in UserSession
        # both UserSession and AnonymousSession need cookies

        # I think I want most of this logic handled in SessionBase

        # I just want SessionManagement to create a new session if needed
        print(f"\n\n self.SESSION_REGISTRY.sessions -- on_request start: {self.SESSION_REGISTRY.sessions}")
        needs_create_session = (
            self.needs_new_session(request=request) or
            self.needs_restore_lost_session(request) or
            len(self.SESSION_REGISTRY.sessions.keys()) == 0
        )
        if needs_create_session:
            print("reached if needs_create_session")
            current_session = self.add_session(request, response)
        else:
            print("reached else")
            current_session = self.get_session(request, response)
        
        if self.needs_registration(request, response):
            current_session = self.do_registration(request, response)
            return "registered?"
        elif self.needs_login(request, response):
            current_session = self.do_login(request, response)
            return "login?"
        elif self.needs_logout(request, response):
            # change to anonymous session
            current_session = self.do_logout(request, response)
            return "loggedout?"


        print(f"\n\n self.SESSION_REGISTRY.sessions -- on_request end: {self.SESSION_REGISTRY.sessions}")
        return current_session.handle_request(request, response)

    def needs_registration(self, request, response) -> bool:
        url_route = request.path
        if url_route == "/register":
            return True
        return False

    def do_registration(self, request, response) -> UserSession:
        session_pair = self.get_session_pair(request)
        new_user_instance = self.NATIVE_AUTH.register(request, response)
        if new_user_instance:
            session_pair.user_session = UserSession(
                None,
                new_user_instance,
                self.NATIVE_AUTH,
                request,
                response,
                self.DEPLOYMENT,
                self.STORAGE
            )
            response.status_code = 201
            return session_pair.user_session
        else:
            # conflict (ex. duplicate username)
            response.status_code = 409

    def needs_login(self, request, response) -> bool:
        url_route = request.path
        if url_route == "/login":
            return True
        return False

    def do_login(self, request, response) -> UserSession:
        session_pair = self.get_session_pair(request)
        user_instance = self.NATIVE_AUTH.login(request, response)
        if user_instance:
            session_pair.user_session = UserSession(
                None,
                user_instance,
                self.NATIVE_AUTH,
                request,
                response,
                self.DEPLOYMENT,
                self.STORAGE
            )
            response.status_code = 200
            return session_pair.user_session
        else:
            # invalid credentials
            response.status_code = 401

    def needs_logout(self, request, response) -> bool:
        url_route = request.path
        if url_route == "/logout":
            return True
        return False

    def do_logout(self, request, response) -> UserSession:
        session_pair = self.get_session_pair(request)
        user_session = session_pair.user_session
        #self.NATIVE_AUTH.logout(request, response)
        if not user_session.authenticate_cookies(request, response):
            # Invalid credentials
            response.status_code = 401
            return "error"
        
        user_session.clear_cookie(request, response)
        session_pair.user_session = None
        response.status_code = 200
        # TODO: do i ever need to make a new Anonymous Session?
        results = {}
        results["session_token"] = session_pair.anonymous_session.token
        attach_data_to_payload(response, results)
        return session_pair.anonymous_session

    def exit_session(self, user_info, session_info):
        self.authenticate_user(user_info, session_info)
        self.current_state[session_info] = None

        # clear token hash
        # clear users set
        return

    def exit_session_admin(self, user_info):
        user_id = user_info["id"]
        session_info = self.generate_token(user_info)
        self.current_state[session_info] = None

        # clear token hash
        # clear users set (self.current_users)
        self.current_users.remove(user_id)
        return
