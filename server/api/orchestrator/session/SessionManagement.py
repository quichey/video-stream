from dataclasses import dataclass
from typing import Optional

from api.orchestrator.session.Session import SessionBase
from api.orchestrator.session.AnonymousSession import AnonymousSession
from api.orchestrator.session.UserSession import UserSession
from api.util.request_data import has_user_info, extract_long_term_cookie
from api.util.cookie import generate_cookie
from auth.native.native import NativeAuth

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
        self.LONG_TERM_COOKIE_ID = generate_cookie("long_term_cookie_id", self.DEPLOYMENT, response)
        return self.LONG_TERM_COOKIE_ID

    def create_user_session(self, request, response, deployment, storage):
        self.user_session = UserSession(request, response, deployment, storage)
        return self.user_session

 
@dataclass
class SessionRegistry:
    # str should be cookie_id
    sessions: dict[str, SessionPair]

class SessionManagement():
    SESSION_REGISTRY = SessionRegistry(sessions={})
    DEPLOYMENT = None
    STORAGE = None
    NATIVE_AUTH = None

    def __init__(self, deployment, storage):
        self.DEPLOYMENT = deployment
        self.STORAGE = storage
        self.NATIVE_AUTH = NativeAuth(self.DEPLOYMENT)
    
    def add_session(self, request, response):
        new_session = AnonymousSession(request, response, self.DEPLOYMENT, self.STORAGE)
        session_pair = SessionPair(
            anonymous_session=new_session
        )
        session_uuid = session_pair.create_cookie(request, response, self.DEPLOYMENT)
        self.SESSION_REGISTRY.sessions[session_uuid] = session_pair
        return new_session

    def end_session(self, request):
        pass

    def get_session_pair(self, request) -> SessionPair:
        long_term_cookie_id = extract_long_term_cookie(request)
        print(f"\n\n self.SESSIONS: {self.SESSIONS}")
        session_pair = self.SESSION_REGISTRY.sessions.get(long_term_cookie_id)
        return session_pair


    def get_session(self, request) -> SessionBase:
        session_pair = self.get_session_pair(request)
        user_info_exists = has_user_info(request)
        if user_info_exists:
            return session_pair.user_session
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
        if self.needs_new_session(request=request) or self.needs_restore_lost_session(request):
            current_session = self.add_session(request, response)
        else:
            current_session = self.get_session(request=request)
        
        if self.needs_registration(request, response):
            current_session = self.do_registration(request, response)
            return "registered?"


        print(f"\n\n self.SESSION_REGISTRY.sessions -- on_request end: {self.SESSION_REGISTRY.sessions}")
        return current_session.handle_request(request, response)

    def needs_registration(self, request, response) -> bool:
        url_route = request.path
        if url_route == "/register":
            return True
        return False

    def do_registration(self, request, response) -> UserSession:
        session_pair = self.get_session_pair(request)
        session_pair.user_session = UserSession(
            self.NATIVE_AUTH,
            request,
            response,
            self.DEPLOYMENT,
            self.STORAGE
        )
        return session_pair.user_session

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
