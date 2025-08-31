from abc import ABC, abstractmethod
from flask import make_response
import uuid
import json

from api.orchestrator.session.state.upload_video import VideoUpload
from api.orchestrator.session.state.watch_video import Video
from api.orchestrator.session.state.home import Home
from api.util.request_data import (
    extract_session_token,
    has_session_token,
    has_long_term_cookie,
    attach_data_to_payload
)
from api.util.error_handling import SecurityError

def post_load_session_hook(func):
    """Decorator to run a step if the subclass/provider defines it."""
    def wrapper(self, *args, **kwargs):
        ret_val = func(self, *args, **kwargs)
        # Call post_load_session step if provider has it
        post_load_session = getattr(self, "post_load_session", None)
        if callable(post_load_session):
            post_load_session(*args, **kwargs)
        return ret_val
    return wrapper

class SessionBase(ABC):
    DEPLOYMENT = None
    STORAGE = None

    TOKEN = None

    VIDEO = None
    VIDEO_UPLOAD = None
    HOME = None

    def __init__(self, request, response, deployment, storage):
        self.DEPLOYMENT = deployment
        self.STORAGE = storage
        self.generate_token(request, response)


    def authenticate_cookies(self, request, response):
        # TODO: Verify LONG_TERM_COOKIE_ID matches from request
        # Verify TEMP_COOKIE_ID matches from request
        
        # Handle temp cookie
        request_session_token = extract_session_token(request)
        request_session_token_exists = has_session_token(request)
        if request_session_token_exists and (request_session_token != self.TOKEN):
            raise SecurityError("Hijacked Session Token")

        # Handle User refresh web-page
        self.handle_new_temp_session(request, response)

        return "ok"
    
    def handle_new_temp_session(self, request, response):
        # needed  and (self.TEMP_COOKIE_ID is None)
        # so that first request did not generate 2 temp_cookies
        # but also want to generate new temp_cookie of no temp_cookie from request
        # for case where user reloads the page
        #
        # Assume for now that long_term_cookie lasts forever
        # for first instance of session, long_term_cookie and temp_cookie do not exist in request
        # So to handle case of refreshing page, long_term_cookie should be present but short_term_cookie
        # should not be present
        request_long_term_cookie_id_exists = has_long_term_cookie(request)
        request_session_token_exists = has_session_token(request)
        need_temp_cookie = (not request_session_token_exists) and (request_long_term_cookie_id_exists)
        if need_temp_cookie:
            return self.generate_token(request, response)


    def determine_event(self, request):
        url_route = request.path
        if url_route == "/load-session":
            return "load_session"
        if url_route == "/video":
            return "watch_video"
        elif url_route == "/getcomments":
            return "get_comments"
        elif url_route == "/video-list":
            return "home"
        elif url_route == "/upload-profile-pic":
            return "upload-profile-pic"
    
    @post_load_session_hook
    def load_session(self, request, response, results):
        results["session_token"] = self.handle_new_temp_session(request, response) or self.TOKEN

    def handle_request(self, request, response):
        self.authenticate_cookies(request, response)
        event = self.determine_event(request)
        results = {}
        match event:
            case "load_session":
                self.load_session(request, response, results)
            case "watch_video":
                self.VIDEO = Video(request, response, self.DEPLOYMENT, self.STORAGE)
                video_data = self.VIDEO.open_video(request, response)
                results["video_data"] = video_data
            case "get_comments":
                comment_data = self.VIDEO.comments.get_comments(request, response)
                results["comment_data"] = comment_data
            case "video_upload":
                self.VIDEO_UPLOAD = VideoUpload(request, response, self.DEPLOYMENT, self.STORAGE)
            case "home":
                self.HOME = Home(request, response, self.DEPLOYMENT, self.STORAGE)
                video_list_data = self.HOME.get_video_list(request, response)
                results["video_list"] = video_list_data
            case "upload-profile-pic":
                self.upload_profile_pic(request, response)
        print(f"\n\n resultsL {results} \n\n")
        
        attach_data_to_payload(response, results)
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


    def generate_token(self, request, response):
        token = self.generate_uuid()
        self.TOKEN = token
        self.refresh_state()
        return token
    
    def refresh_state(self):
        # use case: user reloads webpage
        pass