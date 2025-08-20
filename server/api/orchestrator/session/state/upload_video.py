from state.state_module import StateModule

from api.util.request_data import extract_video_file_info

VIDEO_UPLOAD_PAGE_SIZE = 6400000


class VideoUpload(StateModule):
    name: str
    byte_stream: bytes
    is_done: bool

    def __init__(self, request, response):
        video_file_info = extract_video_file_info(request=request)
        self.name = video_file_info["name"]
        self.byte_stream = video_file_info["byte_stream"]
        self.is_done = video_file_info["is_done"]

        
        return


    """
    as of now, largest sample video works w/one server request
    but most likely i think need multiple for multiple gig sized files
    """
    def video_upload(self, request, response):
        #token = existing_session_info
        #user_state = self.current_state[token]
#
        #if user_state.video_upload is None:
        #    video_upload_session = self.start_video_upload(
        #        existing_session_info=existing_session_info,
        #        video_upload_info=video_upload_info,
        #    )
        #else:
        #    video_upload_session = self.continue_video_upload(
        #        existing_session_info=existing_session_info,
        #        video_upload_info=video_upload_info,
        #    )
#
        #return video_upload_session
        return
    
    def start_video_upload(self, request, response):
        #token = existing_session_info
        #user_state = self.current_state[token]
        #is_done=False
        #if len(self.bytes) < VIDEO_UPLOAD_PAGE_SIZE:
        #    is_done = True
        #user_state.video_upload = VideoUpload(
        #    name=video_upload_info.name,
        #    byte_stream=video_upload_info.bytes,
        #    is_done=is_done
        #)
        #self.current_state[token] = user_state
        #return user_state.video_upload
        return
    
    def continue_video_upload(self, request, response):
        #token = existing_session_info
        #user_state = self.current_state[token]
        #user_state.video_upload.byte_stream += video_upload_info.bytes
        #if len(video_upload_info.bytes) < VIDEO_UPLOAD_PAGE_SIZE:
        #    user_state.video_upload.is_done = True
        #return user_state.video_upload
        return
   
    