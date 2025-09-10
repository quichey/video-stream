from typing import Optional
from api.util.cookie import generate_cookie

from api.orchestrator.session.tab_session.TabSession import TabSession
from api.orchestrator.session.tab_session.AnonymousTabSession import (
    AnonymousTabSession,
)
from api.orchestrator.session.tab_session.UserTabSession import UserTabSession
from api.util.request_data import (
    has_user_session_cookie,
    attach_data_to_payload,
)

from api.util.db_engine import DataBaseEngine
from auth.ThirdPartyAuth import ThirdPartyAuth
from auth.native.native import NativeAuth
from auth.authorizor.Authorizor import Authorizor


class BrowserSession(DataBaseEngine):
    anonymous_tab_session: AnonymousTabSession
    user_tab_session: Optional[UserTabSession] = None
    LONG_TERM_COOKIE_ID: str = None
    AUTHORIZOR: Authorizor = None

    def __init__(self, request, response):
        self.anonymous_tab_session = AnonymousTabSession(request, response)
        self.create_cookie(request, response)

    def create_cookie(self, request, response):
        return self.generate_long_term_cookie(request, response)

    def generate_long_term_cookie(self, request, response):
        self.LONG_TERM_COOKIE_ID = generate_cookie("long_term_session", response)
        return self.LONG_TERM_COOKIE_ID

    def create_user_tab_session(self, request, response):
        self.user_tab_session = UserTabSession(request, response)
        return self.user_tab_session

    def restore_lost_user_tab_session(self, request, response) -> UserTabSession:
        has_user_cookie = has_user_session_cookie(request)
        if has_user_cookie:
            # TODO: what if user_tab_session is empty? create user_tab_session
            # need to return session_token, i think already handled
            # TODO: return user's info on /load-session api
            # ----- name, profile pic info
            if not self.user_tab_session:
                print("\n\n got here: if not session_pair.user_tab_session \n\n")
                self.AUTHORIZOR = Authorizor(NativeAuth)
                user_record = self.AUTHORIZOR.restore_lost_session(request, response)
                self.user_tab_session = UserTabSession(
                    user_record,
                    request,
                    response,
                )

            return self.user_tab_session

    def do_registration(self, request, response) -> UserTabSession:
        self.AUTHORIZOR = Authorizor(NativeAuth)
        new_user_instance = self.AUTHORIZOR.handle_register(request, response)
        if new_user_instance:
            self.user_tab_session = UserTabSession(
                new_user_instance,
                request,
                response,
            )
            response.status_code = 201
            return self.user_tab_session
        else:
            # conflict (ex. duplicate username)
            response.status_code = 409

    def do_login(self, request, response) -> UserTabSession:
        self.AUTHORIZOR = Authorizor(NativeAuth)
        user_instance = self.AUTHORIZOR.handle_login(request, response)
        if user_instance:
            self.user_tab_session = UserTabSession(
                user_instance,
                request,
                response,
            )
            response.status_code = 200
            return self.user_tab_session
        else:
            # invalid credentials
            response.status_code = 401

    def do_logout(self, request, response) -> UserTabSession:
        succeeded = self.AUTHORIZOR.handle_logout(request, response)
        if succeeded:
            self.AUTHORIZOR = None
            self.user_tab_session = None
            response.status_code = 200
            # TODO: do i ever need to make a new Anonymous Session?
            results = {}
            results["session_token"] = self.anonymous_tab_session.token
            attach_data_to_payload(response, results)
            return self.anonymous_tab_session

    def do_third_party_login(self, request, response) -> UserTabSession:
        self.AUTHORIZOR = Authorizor(ThirdPartyAuth)
        user_instance = self.AUTHORIZOR.handle_third_party_auth(request, response)
        print(f"\n\n do_third_party_login user_instance: {user_instance} \n\n")
        if user_instance:
            self.user_tab_session = UserTabSession(
                user_instance,
                request,
                response,
            )
            print(
                f"\n\n do_third_party_login self.user_tab_session: {self.user_tab_session} \n\n"
            )
            response.status_code = 200
            return self.user_tab_session
        else:
            # invalid credentials
            response.status_code = 401

    def needs_registration(self, request, response) -> bool:
        url_route = request.path
        if url_route == "/register":
            return True
        return False

    def needs_login(self, request, response) -> bool:
        url_route = request.path
        if url_route == "/login":
            return True
        return False

    def needs_logout(self, request, response) -> bool:
        url_route = request.path
        if url_route == "/logout":
            return True
        return False

    def needs_third_party_login(self, request, response) -> bool:
        url_route = request.path
        third_party_auth_routes = ["/auth/google/callback", "/auth/facebook/callback"]
        if url_route in third_party_auth_routes:
            return True
        return False

    def get_session(self, request, response) -> TabSession:
        has_user_cookie = has_user_session_cookie(request)
        if has_user_cookie:
            if not self.user_tab_session:
                return self.restore_lost_user_tab_session(request, response)
            else:
                return self.user_tab_session
        else:
            return self.anonymous_tab_session

    def on_request(self, request, response):
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
        elif self.needs_third_party_login(request, response):
            # change to anonymous session
            current_session = self.do_third_party_login(request, response)
            return "google-login?"
        current_session = self.get_session(request, response)
        if self.AUTHORIZOR is not None:
            self.AUTHORIZOR.authenticate(request, response)
        current_session.handle_request(request, response)
