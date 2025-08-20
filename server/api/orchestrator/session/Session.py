from abc import ABC, abstractmethod
from flask import make_response
import uuid

from state.upload_video import VideoUpload
from state.watch_video import Video


class SessionBase(ABC):
    LONG_TERM_COOKIE_ID = None
    TEMP_COOKIE_ID = None
    VIDEO = None
    VIDEO_UPLOAD = None

    def __init__(self):
        self.generate_long_term_cookie()
        self.generate_temp_cookie()


    def authenticate_cookies(self, request):
        # TODO: Verify LONG_TERM_COOKIE_ID matches from request
        # Verify TEMP_COOKIE_ID matches from request
        long_term_cookie_id = request.cookies.get("long_term_session")
        if long_term_cookie_id != self.LONG_TERM_COOKIE_ID:
            raise SecurityError("Hijacked Session Token")
        temp_cookie_id = request.cookies.get("temp_session")
        if temp_cookie_id != self.TEMP_COOKIE_ID:
            raise SecurityError("Hijacked Session Token")
        return "ok"

    def handle_request(self, request):
        self.authenticate_cookies(request=request)
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

    def generate_uuid(self):
        uuid = str(uuid.uuid4())
        return uuid

    def generate_long_term_cookie(self):
        resp = make_response("Cookie is set")
        long_term_cookie_id = self.generate_uuid()
        self.TEMP_COOKIE_ID = long_term_cookie_id
        resp.set_cookie(
            "long_term_session",
            long_term_cookie_id,
            max_age=30*24*60*60,  # 30 days in seconds
            httponly=True,
            secure=True  # only over HTTPS
        )
        return resp

    def generate_temp_cookie(self):
        resp = make_response("Cookie is set")
        temp_cookie_id = self.generate_uuid()
        self.TEMP_COOKIE_ID = temp_cookie_id
        resp.set_cookie(
            "temp_session",
            temp_cookie_id,
            max_age=60*60,  # 1 hour in seconds
            httponly=True,
            secure=True
        )
        return resp