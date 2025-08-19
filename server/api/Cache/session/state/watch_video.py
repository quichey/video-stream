from state.comments import Comments

@dataclass
class Video:
    id: int
    timestamp: str
    comments: Comments

    def __init__(self, existing_session_info, video_info):
        self.id=video_info["id"]
        self.timestamp=0,
        self.comments=Comments()
        return