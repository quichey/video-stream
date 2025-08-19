from dataclasses import dataclass
from typing import Optional


@dataclass
class Comments:
    offset: int
    limit: int
    next_page: bool

    def get_state(self):
        return self.state

    def update_state(self, key, value):
        self.state[key] = value

    def update_state(self, session_info, domain, key, value, subdomain=None):
        state_of_session = self.get_state(session_info, domain, subdomain)
        
        if subdomain == "comments" and key == "offset":
            if state_of_session.next_page is False:
                state_of_session.next_page = True # might not need this flag anymore
                state_of_session.limit = COMMENTS_NEXT_PAGE_SIZE

        #TODO: consider changing session_info into self.extract_id(session_info)
        setattr(state_of_session, key, value)
        return

        # regression test
    def start_video_session(self, existing_session_info, video_info):
        token = existing_session_info
        user_state = self.current_state[token]
        user_state.video = Video(
            id=video_info["id"],
            timestamp=0,
            comments=Comments(
                limit=COMMENTS_FIRST_PAGE_SIZE,
                offset=0,
                next_page=False
            )
        )
        self.current_state[token] = user_state
        return existing_session_info