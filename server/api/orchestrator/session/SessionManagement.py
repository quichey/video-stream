from dataclasses import dataclass

from api.orchestrator.session.browser_session.BrowserSession import (
    BrowserSession,
)
from api.util.request_data import (
    has_user_info,
    extract_long_term_cookie,
)


class SecurityError(Exception):
    pass


@dataclass
class SessionRegistry:
    # str should be LONG_TERM_COOKIE_ID
    sessions: dict[str, BrowserSession]


class SessionManagement:
    SESSION_REGISTRY = None

    def __init__(self):
        self.SESSION_REGISTRY = SessionRegistry(sessions={})

    def add_browser_session(self, request, response) -> BrowserSession:
        new_session_pair = BrowserSession(request, response)
        self.SESSION_REGISTRY.sessions[new_session_pair.LONG_TERM_COOKIE_ID] = (
            new_session_pair
        )
        return new_session_pair

    def end_session(self, request):
        pass

    def get_browser_session(self, request) -> BrowserSession:
        long_term_cookie_id = extract_long_term_cookie(request)
        # print(f"\n\n self.SESSIONS: {self.SESSIONS}")
        session_pair = self.SESSION_REGISTRY.sessions.get(long_term_cookie_id)
        return session_pair

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

    def on_request(self, request, response, SESSION_TOKEN_HACK=None):
        if SESSION_TOKEN_HACK is not None:
            browser_session_list = self.SESSION_REGISTRY.sessions.values()
            TEMP_LONG_TERM_SESSION_HACK = None
            for one_browser_session in browser_session_list:
                anon_session = one_browser_session.anonymous_tab_session
                if anon_session.token == SESSION_TOKEN_HACK:
                    TEMP_LONG_TERM_SESSION_HACK = (
                        one_browser_session.LONG_TERM_COOKIE_ID
                    )
                    break
            browser_session = self.SESSION_REGISTRY.sessions.get(
                TEMP_LONG_TERM_SESSION_HACK
            )
            return browser_session.on_request(request, response)
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
        print(
            f"\n\n self.SESSION_REGISTRY.sessions -- on_request start: {self.SESSION_REGISTRY.sessions}"
        )
        needs_create_session = (
            self.needs_new_session(request=request)
            or self.needs_restore_lost_session(request)
            or len(self.SESSION_REGISTRY.sessions.keys()) == 0
        )
        if needs_create_session:
            print("reached if needs_create_session")
            browser_session = self.add_browser_session(request, response)
        else:
            print("reached else")
            browser_session = self.get_browser_session(request)

        print(
            f"\n\n self.SESSION_REGISTRY.sessions -- on_request end: {self.SESSION_REGISTRY.sessions}"
        )
        return browser_session.on_request(request, response)

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
