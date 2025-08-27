from sqlalchemy.orm import Session
from datetime import datetime

from api.orchestrator.session.state.state_module import StateModule

from api.util.request_data import extract_user_info

from auth.Auth import Auth

VIDEO_UPLOAD_PAGE_SIZE = 6400000


"""
Maybe just put Auth in orchestrator?
and get rid of this one?
"""

class Register(StateModule):
    AUTH = None

    def __init__(self, request, response, deployment, storage):
        super().__init__(request, response, deployment, storage)
        self.AUTH = Auth()
        user_info = extract_user_info(request)
        if user_info and user_info.get('id'):
            self.user_id = user_info.get('id')
        else:
            #TODO: think of what to do for anonymous users
            self.user_id = 1
        return

    def register_user(self, request, response):
        credentials = self.AUTH.handle_request(request, response)

    def store_video(self, request, response):
        """
        check if user has started a VideoUpload session
        if not, start one,
        else, continue.

        if reached 0 bytes, store the video
        """
        #video_upload_session = self.session_manager.video_upload(
        #    session_info,
        #    video_upload_info=video_file_info
        #)
        #if not video_upload_session.is_done:
        #    return video_upload_session.is_done

        #TODO: copy to client/public/videos folder
        video = Video(
            user_id=self.user_id,
            file_dir=self.user_id,
            file_name=self.name,
            date_created=datetime.now(),
            date_updated=datetime.now(),
        )
        self.manager.store_video(
            video_record=video,
            seeding_db=False,
            byte_stream=self.byte_stream
        )
        # also save to mysql db
        with Session(self.engine) as session:
            session.add(video)
            session.commit()
            
        #return self.is_done
        return True