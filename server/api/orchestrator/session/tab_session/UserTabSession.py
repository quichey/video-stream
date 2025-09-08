from sqlalchemy.orm import Session

from server.api.orchestrator.session.tab_session.TabSession import TabSession

from api.util.request_data import (
    attach_data_to_payload,
    extract_profile_pic_info,
)
from db.Schema.Models import User
from api.util.db_engine import DataBaseEngine
from api.orchestrator.storage import STORAGE


class UserTabSession(TabSession, DataBaseEngine):
    USER_INSTANCE: User = None

    def __init__(
        self,
        user_instance: User,
        request,
        response,
    ):
        TabSession.__init__(self, request, response)
        self.USER_INSTANCE = user_instance
        self.return_user_data(request, response)

    # return user data
    def return_user_data(self, request, response):
        results = {}
        self.post_load_session(request, response, results)
        attach_data_to_payload(response, results)

    def post_load_session(self, request, response, results):
        profile_icon_sas_url = STORAGE.get_image_url(
            self.USER_INSTANCE.id, self.USER_INSTANCE.profile_icon
        )
        results["user_data"] = {
            "id": self.USER_INSTANCE.id,
            "name": self.USER_INSTANCE.name,
            "email": self.USER_INSTANCE.email,
            "profile_icon": self.USER_INSTANCE.profile_icon,
            "profile_icon_sas_url": profile_icon_sas_url,
        }

    def get_token(self):
        return self.token

    def get_state(self):
        return self.state

    def update_state(self, key, value):
        self.state[key] = value
        # persist to DB

    def upload_profile_pic(self, request, response):
        pic_info = extract_profile_pic_info(request)
        file_name = pic_info["file_name"]
        byte_stream = pic_info["byte_stream"]
        user_id = self.USER_INSTANCE.id
        sas_url = STORAGE.store_image(user_id, file_name, byte_stream)
        succeeded = self.update_pic_db(file_name)
        if succeeded and sas_url:
            return {"profile_icon": file_name, "profile_icon_sas_url": sas_url}
        # TODO: return new sasURLS so client updates all images

    def update_pic_db(self, file_name) -> bool:
        self.USER_INSTANCE.profile_icon = file_name
        try:
            with Session(self.engine) as session:
                session.merge(self.USER_INSTANCE)  # re-attaches it
                session.commit()
            return True
        except Exception as e:
            # optionally log the exception
            print(f"Failed to update profile icon: {e}")
            return False

    def remove_profile_pic(self, request, response):
        self.USER_INSTANCE.profile_icon = None
        try:
            with Session(self.engine) as session:
                session.merge(self.USER_INSTANCE)  # re-attaches it
                session.commit()
            response.status_code = 200
            return {"success": True}
        except Exception as e:
            # optionally log the exception
            print(f"Failed to remove profile icon: {e}")
            response.status_code = 500
            return {"success": False}
