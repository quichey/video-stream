from api.orchestrator.session.Session import SessionBase

class SecurityError(Exception):
    pass

class UserSession(SessionBase):
    AUTH_COOKIE = None
    def __init__(self, user_id: int):
        self.token = f"user-{user_id}"
        self.state = {}  # could be from DB/cache
    
    def generate_auth_cookie(self, request, response):
        pass

    def get_token(self):
        return self.token

    def get_state(self):
        return self.state

    def update_state(self, key, value):
        self.state[key] = value
        # persist to DB
