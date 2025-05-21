from dataclasses import dataclass

COMMENTS_FIRST_PAGE_SIZE = 15
COMMENTS_NEXT_PAGE_SIZE = 10


class SecurityError(Exception):
    pass

@dataclass
class Comments:
    offset: int
    limit: int
    next_page: bool

@dataclass
class Video:
    id: int
    timestamp: str
    comments: Comments

@dataclass
class User:
    id: int
    token: int
    video: Video

"""
NOTE: possible datastructure involving the dataclasses above
TODO: consider what the actual code is going to be like to update state
NOTE: session_info is primitive/literal token value
self.state = {
    "token_1": User(
        id: user_id_1
        token: token_1
        video: Video(
            id: 1
            timestamp: 0
            comments: Comments(
                offset: 0
                limit: 10
            )
        )
    ),
    "token_2": User(
        id: user_id_2
        token: token_2
        video: Video(
            id: 1
            timestamp: 0
            comments: Comments(
                offset: 0
                limit: 10
            )
        )
    )
}
"""

"""
TODO: Need to keep track of user's current video_id that is viewed
so know when to clear the comments_state
-- decide whether to require that video_id param in get_session or not
"""

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
        print(f"user_id: {user_id}")
        print(f"existing_session_info: {existing_session_info}")
        print(f"type(user_id): {type(user_id)}")
        print(f"type(existing_session_info): {type(existing_session_info)}")
        if int(user_id) != int(existing_session_info):
            raise SecurityError("Hijacked Session Token")
        return existing_session_info
    
    def register_user(self, user_info, existing_session_info, video_info):
        user_id = user_info["id"]
        # TODO: Check if user_info matches existing_session_info,
        # otherwise throw a security error
        if existing_session_info is not None:
            return self.authenticate_user(user_info, existing_session_info)

        print(f"self.current_users: {self.current_users}")
        if user_id in self.current_users:
            raise Exception("User already registered")
        
        token = self.generate_token(user_info)
        self.user_tokens.append([user_id, token])
        self.current_users.add(user_id)
        user_state = User(
            id=user_id,
            token=token,
            video=Video(
                id=video_info["id"],
                timestamp=0,
                comments=Comments(
                    limit=COMMENTS_FIRST_PAGE_SIZE,
                    offset=0,
                    next_page=False
                )
            )
        )
        self.current_state[token] = user_state
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
    def get_state(self, session_info, domain, subdomain = None):
        if session_info not in self.current_state.keys():
            raise SecurityError()
        try:
            state_of_session = getattr(self.current_state[session_info], domain)
            if subdomain is not None:
                state_of_session = getattr(state_of_session, subdomain)
        except Exception as e:
            raise e
        #print(f"\n\n get_state state_of_session: {state_of_session} \n\n")
        return state_of_session
    
    def update_state(self, session_info, domain, key, value, subdomain=None):
        state_of_session = self.get_state(session_info, domain, subdomain)
        
        if subdomain == "comments" and key == "offset":
            if state_of_session.next_page is False:
                state_of_session.next_page = True # might not need this flag anymore
                state_of_session.limit = COMMENTS_NEXT_PAGE_SIZE

        #TODO: consider changing session_info into self.extract_id(session_info)
        setattr(state_of_session, key, value)
        return
    
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
