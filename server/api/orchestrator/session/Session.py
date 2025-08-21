from abc import ABC, abstractmethod
from flask import make_response
from datetime import datetime
import uuid
import json

from api.orchestrator.session.state.upload_video import VideoUpload
from api.orchestrator.session.state.watch_video import Video
from api.orchestrator.session.state.home import Home
from api.util.request_data import extract_temp_cookie, has_temp_cookie, has_long_term_cookie, extract_long_term_cookie
from api.util.error_handling import SecurityError


class SessionBase(ABC):
    DEPLOYMENT = None

    LONG_TERM_COOKIE_ID = None
    TEMP_COOKIE_ID = None
    VIDEO = None
    VIDEO_UPLOAD = None
    HOME = None

    def __init__(self, request, response, deployment):
        self.DEPLOYMENT = deployment
        self.generate_long_term_cookie(request, response)
        self.generate_temp_cookie(request, response)


    def authenticate_cookies(self, request, response):
        # TODO: Verify LONG_TERM_COOKIE_ID matches from request
        # Verify TEMP_COOKIE_ID matches from request

        # Handle long term cookie
        long_term_cookie_id = extract_long_term_cookie(request)
        long_term_cookie_id_exists = has_long_term_cookie(request)
        if long_term_cookie_id_exists and (long_term_cookie_id != self.LONG_TERM_COOKIE_ID):
            raise SecurityError("Hijacked Long Term Cookie")
        
        # Handle temp cookie
        temp_cookie_id = extract_temp_cookie(request)
        temp_cookie_id_exists = has_temp_cookie(request)
        if temp_cookie_id_exists and (temp_cookie_id != self.TEMP_COOKIE_ID):
            raise SecurityError("Hijacked Session Token")
        need_temp_cookie = (not temp_cookie_id_exists) and (self.TEMP_COOKIE_ID is None)
        if need_temp_cookie:
            self.generate_temp_cookie(request, response)


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
        self.authenticate_cookies(request, response)
        event = self.determine_event(request)
        results = {}
        match event:
            case "watch_video":
                self.VIDEO = Video(request, response, self.DEPLOYMENT)
                video_data = self.VIDEO.open_video(request, response)
                results["video_data"] = video_data
            case "get_comments":
                comments_data = self.VIDEO.comments.get_comments(request, response)
                results["comments_data"] = comments_data
            case "video_upload":
                self.VIDEO_UPLOAD = VideoUpload(request, response, self.DEPLOYMENT)
            case "home":
                self.HOME = Home(request, response, self.DEPLOYMENT)
                video_list_data = self.HOME.get_video_list(request, response)
                results["video_list"] = video_list_data
        print(f"\n\n resultsL {results} \n\n")
        def datetime_handler(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()  # or str(obj)
            raise TypeError("Type not serializable")
        response.data = json.dumps(results, default=datetime_handler)
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

    def generate_long_term_cookie(self, request, response):
        long_term_cookie_id = self.generate_uuid()
        self.LONG_TERM_COOKIE_ID = long_term_cookie_id
        response.set_cookie(
            "long_term_session",
            long_term_cookie_id,
            max_age=30*24*60*60,  # 30 days in seconds
            httponly=True,
            secure=True  # only over HTTPS
        )
        return response

    def generate_temp_cookie(self, request, response):
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