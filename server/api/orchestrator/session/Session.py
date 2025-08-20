from abc import ABC, abstractmethod
from flask import make_response
import uuid
import json

from api.orchestrator.session.state.upload_video import VideoUpload
from api.orchestrator.session.state.watch_video import Video
from api.orchestrator.session.state.home import Home
from api.util.request_data import extract_temp_cookie, has_temp_cookie
from api.util.error_handling import SecurityError


class SessionBase(ABC):
    LONG_TERM_COOKIE_ID = None
    TEMP_COOKIE_ID = None
    VIDEO = None
    VIDEO_UPLOAD = None
    HOME = None

    def __init__(self, request):
        self.generate_long_term_cookie(request)
        self.generate_temp_cookie(request)


    def authenticate_cookies(self, request):
        # TODO: Verify LONG_TERM_COOKIE_ID matches from request
        # Verify TEMP_COOKIE_ID matches from request

        # Handle long term cookie
        long_term_cookie_id = request.cookies.get("long_term_session")
        if long_term_cookie_id != self.LONG_TERM_COOKIE_ID:
            raise SecurityError("Hijacked Long Term Cookie")
        
        # Handle temp cookie
        temp_cookie_id = extract_temp_cookie(request)
        temp_cookie_id_exists = has_temp_cookie(request)
        if temp_cookie_id_exists and (temp_cookie_id != self.TEMP_COOKIE_ID):
            raise SecurityError("Hijacked Session Token")
        if not temp_cookie_id_exists:
            self.generate_temp_cookie()


        return "ok"

    def determine_event(self, request):
        url_route = request.path
        if url_route == "/video":
            return "watch_video"
        elif url_route == "/getcomments":
            return "get_comments"
        elif url_route == "/video-list":
            return "home"

    def handle_request(self, request, response):
        self.authenticate_cookies(request=request)
        event = self.determine_event(request)
        results = {}
        match event:
            case "watch_video":
                self.VIDEO = Video(request, response)
                response = self.VIDEO.open_video(request, response)
                results["video_data"] = response
            case "get_comments":
                response = self.VIDEO.comments.get_comments(request, response)
                results["comments_data"] = response
            case "video_upload":
                self.VIDEO_UPLOAD = VideoUpload()
            case "home":
                self.HOME = Home(request, response)
                results["video_list"] = self.HOME.get_video_list(request, response)
            
        response.data = json.dumps(results)
        response.content_type = "application/json"
        return response

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
        _uuid = str(uuid.uuid4())
        return _uuid

    def generate_long_term_cookie(self, response):
        long_term_cookie_id = self.generate_uuid()
        self.TEMP_COOKIE_ID = long_term_cookie_id
        response.set_cookie(
            "long_term_session",
            long_term_cookie_id,
            max_age=30*24*60*60,  # 30 days in seconds
            httponly=True,
            secure=True  # only over HTTPS
        )
        return response

    def generate_temp_cookie(self, response):
        temp_cookie_id = self.generate_uuid()
        self.TEMP_COOKIE_ID = temp_cookie_id
        response.set_cookie(
            "temp_session",
            temp_cookie_id,
            max_age=60*60,  # 1 hour in seconds
            httponly=True,
            secure=True
        )
        self.refresh_state()
        return response
    
    def refresh_state(self):
        # use case: user reloads webpage
        pass