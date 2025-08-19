from dataclasses import dataclass
from typing import Optional

from state.comments import Comments
from state.upload_video import VideoUpload
from state.watch_video import Video

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


class SessionBase(ABC):
    TOKEN = None
    VIDEO = Video()
    VIDEO_UPLOAD = VideoUpload()
    COMMENTS = Comments()

    def __init__(self):
        #TODO: IDK how to handle_request?
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

    @abstractmethod
    def authenticate(self, request):
        pass

    def handle_request(self, request):
        pass

    @property
    def key(self):
        pass

    @abstractmethod
    def get_token(self) -> str:
        pass

    @abstractmethod
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
