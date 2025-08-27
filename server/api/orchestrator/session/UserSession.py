from api.orchestrator.session.Session import SessionBase

from api.util.cookie import generate_cookie
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

    def authenticate_cookies(self, request, response):
        pass
