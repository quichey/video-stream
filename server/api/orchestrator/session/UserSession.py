from typing import Literal

from api.orchestrator.session.Session import SessionBase

from api.util.cookie import generate_cookie, expire_cookie
from api.util.error_handling import SecurityError
from api.util.request_data import extract_user_session_cookie, has_user_session_cookie
from db.Schema.Models import User


class UserSession(SessionBase):
    AUTH_COOKIE = None
    NATIVE_AUTH = None
    USER_INSTANCE = None
    def __init__(self, user_instance: User, native_auth, request, response, deployment, storage):
        super().__init__(request, response, deployment, storage)
        self.USER_INSTANCE = user_instance
        self.NATIVE_AUTH = native_auth
        self.generate_auth_cookie(request, response)
    
    def post_load_session(self, request, response, results):
        profile_icon_sas_url = self.STORAGE.get_image_url(
            self.USER_INSTANCE.id,
            self.USER_INSTANCE.profile_icon
        )
        results["user_data"] = {
            "id": self.USER_INSTANCE.id,
            "name": self.USER_INSTANCE.name,
            "email": self.USER_INSTANCE.email,
            "profile_icon": self.USER_INSTANCE.profile_icon,
            "profile_icon_sas_url": profile_icon_sas_url
        }
    
    def generate_auth_cookie(self, request, response):
        self.AUTH_COOKIE = generate_cookie("auth_cookie", self.DEPLOYMENT, response)
        return self.AUTH_COOKIE

    def get_token(self):
        return self.token

    def get_state(self):
        return self.state

    def update_state(self, key, value):
        self.state[key] = value
        # persist to DB

    def authenticate_cookies(self, request, response) -> Literal[True]:
        if not has_user_session_cookie(request):
            raise SecurityError("No User Session Cookie")
        cookie = extract_user_session_cookie(request)
        if cookie != self.AUTH_COOKIE:
            raise SecurityError("Auth Cookie does not Match")
        return True
    
    def clear_cookie(self, request, response):
        expire_cookie("auth_cookie", self.DEPLOYMENT, response)
