from state.comments import Comments
from state.state_module import StateModule


class Video(StateModule):
    id: int
    timestamp: str
    comments: Comments

    def __init__(self, video_info):
        self.id=video_info["id"]
        self.timestamp=0,
        self.comments=Comments()
        return
    
    def open_video(self):
        self.emit("load_first_page_of_comments", {"video_id": self.id})