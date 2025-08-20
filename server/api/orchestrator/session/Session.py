from abc import ABC, abstractmethod

from state.upload_video import VideoUpload
from state.watch_video import Video


class SessionBase(ABC):
    TOKEN = None
    VIDEO = None
    VIDEO_UPLOAD = None

    def __init__(self):
        self.generate_token()

    @abstractmethod
    def authenticate(self, request):
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

    def handle_request(self, request):
        event = pass
        results = {}
        match event:
            case "watch_video":
                video_id = request["video_id"]
                self.VIDEO = Video(id=video_id)
                response = self.VIDEO.open_video(request)
                results["video_data"] = response
            case "get_comments":
                response = self.VIDEO.comments.get_comments(request)
                results["comments_data"] = response
            case "video_upload":
                self.VIDEO_UPLOAD = VideoUpload()
            
            
        return results

    @property
    def key(self):
        pass

    @property
    def token(self) -> str:
        return self.TOKEN
    @token.setter
    def token(self, new_value) -> str:
        self.TOKEN = new_value

    def generate_token(self):
        pass
