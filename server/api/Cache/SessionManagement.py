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

    def __init__(self):
        self.current_users = set()
        self.user_tokens = []
    
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
    
    def exit_session(self, user):
        pass