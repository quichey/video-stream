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
    
    def get_video_data(self, request):
        pass
    def open_video(self, request):
        results = {}
        results["video_data"] = self.get_video_data(request)
        comments_data = self.emit("load_first_page_of_comments", {"video_id": self.id})
        results["comments_data"] = comments_data

        return results
