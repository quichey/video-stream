


class SecurityError(Exception):
    pass



class SessionManagement():
    SESSIONS = {}

    def __init__(self):
        pass
    
    def add_session(self, request):
        pass

    def end_session(self, request):
        pass

    def get_session(self, request):
        pass
    
    def on_request(self, request):
        current_session = self.get_session(request)

        authenticated = current_session.authenticate(request)

        if not authenticated:
            raise SecurityError()
        return current_session.handle_request(request)

    """
    Do i actually need this?
    Wording/concecpt is obviously different from
    register_user. I think I was planning
    on having register_user call this one
    """
    def authenticate_user(self, user_info, existing_session_info):
        user_id = user_info["id"]
        # TODO: Check if user_info matches existing_session_info,
        # otherwise throw a security error
        #print(f"user_id: {user_id}")
        #print(f"existing_session_info: {existing_session_info}")
        #print(f"type(user_id): {type(user_id)}")
        #print(f"type(existing_session_info): {type(existing_session_info)}")
        if int(user_id) != int(existing_session_info):
            raise SecurityError("Hijacked Session Token")
        return existing_session_info

   
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
