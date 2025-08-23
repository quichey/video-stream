class AnonymousSession(SessionBase):
    def __init__(self, server_session_id: str):
        self.token = server_session_id
        self.state = {}  # maybe pulled from Redis or DB

    def get_token(self):
        return self.token

    def get_state(self):
        return self.state

    def update_state(self, key, value):
        self.state[key] = value
        # optionally persist to server
