from typing import Literal
from sqlalchemy.orm import Session

from api.orchestrator.session.Session import SessionBase

from api.util.cookie import generate_cookie, expire_cookie
from api.util.error_handling import SecurityError
from api.util.request_data import (
    extract_user_session_cookie,
    has_user_session_cookie,
    attach_data_to_payload,
    extract_profile_pic_info
)
from db.Schema.Models import User, UserCookie
from api.util.db_engine import DataBaseEngine


class UserSession(SessionBase, DataBaseEngine):
    AUTH_COOKIE = None
    COOKIE_RECORD_ID = None
    NATIVE_AUTH = None
    USER_INSTANCE = None
    def __init__(self, old_cookie: str, user_instance: User, native_auth, request, response, deployment, storage):
        SessionBase.__init__(self, request, response, deployment, storage)
        DataBaseEngine.__init__(self, deployment)
        self.USER_INSTANCE = user_instance
        self.NATIVE_AUTH = native_auth
        if old_cookie:
            self.AUTH_COOKIE = old_cookie
        else:
            self.generate_auth_cookie(request, response)
            self.return_user_data(request, response)

    # return user data
    def return_user_data(self, request, response):
        results = {}
        self.post_load_session(request, response, results)
        attach_data_to_payload(response, results)
    
    def store_cookie_record(self) -> UserCookie | Literal[False]:
        # also save to mysql db
        with Session(self.engine) as session:
            cookie_record = UserCookie(
                user_id=self.USER_INSTANCE.id,
                cookie=self.AUTH_COOKIE,
            )
            session.add(cookie_record)
            session.commit()
            if cookie_record.id is not None:
                self.COOKIE_RECORD_ID = cookie_record.id
                return cookie_record
        
        return False

    def delete_cookie_record(self) -> bool:
        with Session(self.engine) as session:
            rows_deleted = session.query(UserCookie).filter(UserCookie.id == self.COOKIE_RECORD_ID).delete()
            session.commit()

            if rows_deleted > 0:
                return True
            else:
                rows_deleted = session.query(UserCookie).filter(UserCookie.cookie == self.AUTH_COOKIE).delete()
                session.commit()
                if rows_deleted > 0:
                    return True
                else:
                    return False
        return False

    
    def post_load_session(self, request, response, results):
        profile_icon_sas_url = self.STORAGE.get_image_url(
            self.USER_INSTANCE.id,
            self.USER_INSTANCE.profile_icon
        )
        results["user_data"] = {
            "id": self.USER_INSTANCE.id,
            "name": self.USER_INSTANCE.name,
            "email": self.USER_INSTANCE.email,
            "profile_icon": self.USER_INSTANCE.profile_icon,
            "profile_icon_sas_url": profile_icon_sas_url
        }
    
    def generate_auth_cookie(self, request, response):
        self.AUTH_COOKIE = generate_cookie("auth_cookie", self.DEPLOYMENT, response)
        self.store_cookie_record()
        return self.AUTH_COOKIE

    def get_token(self):
        return self.token

    def get_state(self):
        return self.state

    def update_state(self, key, value):
        self.state[key] = value
        # persist to DB

    def authenticate_cookies(self, request, response) -> Literal[True]:
        if not has_user_session_cookie(request):
            raise SecurityError("No User Session Cookie")
        cookie = extract_user_session_cookie(request)
        if cookie != self.AUTH_COOKIE:
            raise SecurityError("Auth Cookie does not Match")
        return True
    
    def clear_cookie(self, request, response):
        expire_cookie("auth_cookie", self.DEPLOYMENT, response)
        self.delete_cookie_record()
        self.AUTH_COOKIE = None

    def upload_profile_pic(self, request, response):
        pic_info = extract_profile_pic_info(request)
        file_name = pic_info["file_name"]
        byte_stream = pic_info["byte_stream"]
        user_id = self.USER_INSTANCE.id
        self.STORAGE.store_image(user_id, file_name, byte_stream)
        self.update_pic_db(file_name)
    
    def update_pic_db(self, file_name):
        self.USER_INSTANCE.profile_icon = file_name
        with Session(self.engine) as session:
            self.USER_INSTANCE = session.merge(self.USER_INSTANCE)  # re-attaches it
            session.commit()