class SessionManagement():
    """
    
    user_tokens = [
        ["user_id_1", "offset_of_user_1"],
        ["user_id_2", "offset_of_user_2"],
        ...
    ]
    """
    user_tokens = None
    current_users = None
    current_state = None
    """
    I think i need to store hashes of the user_tokens that the client program has
    for cybersecurity reasons
    token_hashes = None ?
    """

    def __init__(self, domain="comments"):
        self.current_users = set()
        self.user_tokens = []
        self.domain = domain
        self.current_state = {}
        """
        current_state = [
            {
                "session_id_2": {
                    anything
                }
            },
            {
                "session_id_2": {
                    anything
                }
            },
        ]
        """
    
    def generate_token(self, user_info):
        # TODO: fill in later with actual token generation
        token = user_info["id"]
        return token
    
    def register_user(self, user_info):
        user_id = user_info["id"]
        if user_id in self.current_users:
            raise Exception("User already registered")
        
        token = self.generate_token(user_info)
        self.user_tokens.append([user_id, token])
        self.current_users.add(user_id)
        return token
    
    """
    get all data associated with the session
    probably want to partition this function into separate domains of knowledge
    for latency as well as security
    """
    def get_state(self, session_info):
        return self.current_state[session_info]
    
    def update_state(self, session_info, key, value):
        #TODO: consider changing session_info into self.extract_id(session_info)
        self.current_state[session_info][key] = value
        return
    
    def exit_session(self, user):
        pass

class SecurityError(Exception):
    pass
