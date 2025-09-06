from sqlalchemy.orm import Session
from datetime import datetime

from db.Schema import Video
from db.Schema.Video import VideoFileManager

from api.orchestrator.session.state.state_module import StateModule

from api.util.request_data import extract_video_file_info, extract_user_info

VIDEO_UPLOAD_PAGE_SIZE = 6400000


class VideoUpload(StateModule):
    name: str
    byte_stream: bytes
    is_done: bool
    user_id: int

    manager: VideoFileManager

    def __init__(self, request, response, storage):
        super().__init__(request, response, storage)
        video_file_info = extract_video_file_info(request=request)
        self.name = video_file_info["name"]
        self.byte_stream = video_file_info["byte_stream"]
        self.is_done = video_file_info["is_done"]
        user_info = extract_user_info(request)
        if user_info and user_info.get("id"):
            self.user_id = user_info.get("id")
        else:
            # TODO: think of what to do for anonymous users
            self.user_id = 1

        self.manager = VideoFileManager()
        return

    """
    as of now, largest sample video works w/one server request
    but most likely i think need multiple for multiple gig sized files
    """
    """
    def video_upload(self, request, response):
        token = existing_session_info
        user_state = self.current_state[token]

        if user_state.video_upload is None:
            video_upload_session = self.start_video_upload(
                existing_session_info=existing_session_info,
                video_upload_info=video_upload_info,
            )
        else:
            video_upload_session = self.continue_video_upload(
                existing_session_info=existing_session_info,
                video_upload_info=video_upload_info,
            )

        return video_upload_session
        return
    
    def start_video_upload(self, request, response):
        token = existing_session_info
        user_state = self.current_state[token]
        is_done=False
        if len(self.bytes) < VIDEO_UPLOAD_PAGE_SIZE:
            is_done = True
        user_state.video_upload = VideoUpload(
            name=video_upload_info.name,
            byte_stream=video_upload_info.bytes,
            is_done=is_done
        )
        self.current_state[token] = user_state
        return user_state.video_upload
        return
    
    def continue_video_upload(self, request, response):
        token = existing_session_info
        user_state = self.current_state[token]
        user_state.video_upload.byte_stream += video_upload_info.bytes
        if len(video_upload_info.bytes) < VIDEO_UPLOAD_PAGE_SIZE:
            user_state.video_upload.is_done = True
        return user_state.video_upload
        return
    """

    def store_video(self, request, response):
        """
        check if user has started a VideoUpload session
        if not, start one,
        else, continue.

        if reached 0 bytes, store the video
        """
        # video_upload_session = self.session_manager.video_upload(
        #    session_info,
        #    video_upload_info=video_file_info
        # )
        # if not video_upload_session.is_done:
        #    return video_upload_session.is_done

        # TODO: copy to client/public/videos folder
        video = Video(
            user_id=self.user_id,
            file_dir=self.user_id,
            file_name=self.name,
            date_created=datetime.now(),
            date_updated=datetime.now(),
        )
        self.manager.store_video(
            video_record=video, seeding_db=False, byte_stream=self.byte_stream
        )
        # also save to mysql db
        with Session(self.engine) as session:
            session.add(video)
            session.commit()

        # return self.is_done
        return True
