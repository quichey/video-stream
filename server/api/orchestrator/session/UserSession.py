from api.orchestrator.session.Session import SessionBase

from api.util.cookie import generate_cookie


class UserSession(SessionBase):
    AUTH_COOKIE = None
    def __init__(self, request, response, deployment, storage):
        super().__init__(request, response, deployment, storage)
        self.generate_auth_cookie()
    
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
