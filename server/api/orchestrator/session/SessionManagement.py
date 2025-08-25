from flask import json

from api.orchestrator.session.Session import SessionBase
from api.util.request_data import has_user_info, extract_long_term_cookie

class SecurityError(Exception):
    pass



class SessionManagement():
    SESSIONS = {}
    DEPLOYMENT = None
    STORAGE = None

    def __init__(self, deployment, storage):
        self.DEPLOYMENT = deployment
        self.STORAGE = storage
    
    def add_session(self, request, response):
        new_session = SessionBase(request, response, self.DEPLOYMENT, self.STORAGE)
        session_uuid = new_session.LONG_TERM_COOKIE_ID
        self.SESSIONS[session_uuid] = new_session
        return new_session

    def end_session(self, request):
        pass

    def get_session(self, request):
        long_term_cookie_id = extract_long_term_cookie(request)
        print(f"\n\n self.SESSIONS: {self.SESSIONS}")
        return self.SESSIONS.get(long_term_cookie_id)
    
    def needs_restore_lost_session(self, request):
        long_term_cookie_id = extract_long_term_cookie(request)
        return long_term_cookie_id not in self.SESSIONS.keys()

    def needs_new_session(self, request):
        no_long_term_cookie = not extract_long_term_cookie(request)
        print(f"\n\n request.cookies.get: {extract_long_term_cookie(request)}")
        print(f"\n\n no_long_term_cookie: {no_long_term_cookie}")
        no_user_info = not has_user_info(request)
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
        print(f"\n\n self.SESSIONS -- on_request start: {self.SESSIONS}")
        if self.needs_new_session(request=request) or self.needs_restore_lost_session(request):
            current_session = self.add_session(request, response)
        else:
            current_session = self.get_session(request=request)


        print(f"\n\n self.SESSIONS -- on_request end: {self.SESSIONS}")
        return current_session.handle_request(request, response)

   
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
