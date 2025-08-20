from dataclasses import dataclass
from typing import Optional

from state.state_module import StateModule


COMMENTS_FIRST_PAGE_SIZE = 15
COMMENTS_NEXT_PAGE_SIZE = 10


class Comments(StateModule):
    offset: int = 0
    limit: int = COMMENTS_FIRST_PAGE_SIZE
    next_page: bool = False
    video_id: int = None

    def __init__(self, video_id):
        #self.on_event("load_first_page_of_comments", self.load_first_page)
        self.video_id = video_id

    def get_comments(self):
        # TODO: determine when to do comments_first_page or not
        pass

    """
    def update_state(self, session_info, domain, key, value, subdomain=None):
        state_of_session = self.get_state(session_info, domain, subdomain)
        
        if subdomain == "comments" and key == "offset":
            if state_of_session.next_page is False:
                state_of_session.next_page = True # might not need this flag anymore
                state_of_session.limit = COMMENTS_NEXT_PAGE_SIZE

        #TODO: consider changing session_info into self.extract_id(session_info)
        setattr(state_of_session, key, value)
        return
    """
    def load_next_page(self):
        pass

        # regression test
    def load_first_page(self):

        # TODO: fetch comments?
        # update self.offset
        self.limit = COMMENTS_NEXT_PAGE_SIZE
        self.next_page = True
        return {
            "next_page"
        }