

COMMENTS_FIRST_PAGE_SIZE = 50
COMMENTS_NEXT_PAGE_SIZE = 10


class SecurityError(Exception):
    pass

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

    def __init__(self):
        self.current_users = set()
        self.user_tokens = []
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
        self.current_state[token] = {
            "comments": {}
        }
        return token
    
    """
    get all data associated with the session
    probably want to partition this function into separate domains of knowledge
    for latency as well as security

    implement logic for infinite scroll of comments
    within these two following funcitons.
    How?
    First Page:
        current_state = [
            {
                "session_id_2": {
                    "comments": {
                        "offset": 20,
                        "limit": 30
                    }
                }
            },
            {
                "session_id_2": {
                    anything
                }
            },
        ]
    Next Page:
        current_state = [
            {
                "session_id_2": {
                    "comments": {
                        "offset": 20,
                        "limit": 30,
                        "next_page": True
                    }
                }
            },
            {
                "session_id_2": {
                    anything
                }
            },
        ]


    """
    def get_state(self, session_info, domain):
        state_of_session = self.current_state[session_info][domain]
        if domain == "comments":
            if "limit" not in state_of_session.keys():
                state_of_session["limit"] = COMMENTS_FIRST_PAGE_SIZE
                state_of_session["offset"] = 0
            else:
                state_of_session["limit"] = COMMENTS_NEXT_PAGE_SIZE

        self.current_state[session_info][domain] = state_of_session
        return state_of_session
    
    def update_state(self, session_info, domain, key, value):
        if session_info not in self.current_state.keys():
            raise SecurityError()
        state_of_session = None 

        try:
            state_of_session = self.current_state[session_info][domain]
        except:
            raise Exception()
        
        if domain == "comments" and key == "offset":
            self.current_state[session_info][domain]["next_page"] = True

        #TODO: consider changing session_info into self.extract_id(session_info)
        self.current_state[session_info][domain][key] = value
        return
    
    def exit_session(self, user):
        pass

