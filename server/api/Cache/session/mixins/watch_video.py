

@dataclass
class Video:
    id: int
    timestamp: str
    comments: Comments

    
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