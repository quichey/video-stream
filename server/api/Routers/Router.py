from flask import json
from dataclasses import dataclass

"""
Thinking maybe have this class to handle any common Flask
Logic that I see in ClientRouter and AdminRouter
"""

@dataclass
class VideoUpload:
    name: str
    bytes: bytes
    user_id: int
    upload_date: str

class Router():
    def __init__(self, app, cache, request):
        self.cache = cache
        self.request = request

        self.set_up()
        self.construct_routes(app, request)
    

    def extract_user_info(self):
        form_data = json.loads(self.request.data)
        # TODO: change later to something like request.form['username']
        user_info = {
            "id": form_data['user_id'],
            "name": form_data['user_name']
        }
        return user_info

    
    def extract_video_info(self):
        form_data = json.loads(self.request.data)
        video_info = {}
        if "video_id" in form_data:
            video_info["id"] = form_data['video_id']
        return video_info


    """
    TODO: at some point
    implement way to handle chunked data
    """
    def extract_video_file_info(self):
        user_info = self.extract_user_info()
        print(f"\n\n reached extract_video_file_info \n\n")
        form_data = json.loads(self.request.data)
        video_file_info = {}
        if "file_info" in form_data:
            file_info = form_data['file_info']
            print(f"\n\n file_info: {file_info} \n\n")
            file_stream = dict(file_info["file_stream"])
            print(f"\n\n len(file_stream.keys()): {len(file_stream.keys())} \n\n")
            file_name = file_info["name"]
            # file being loaded as str
            # convert to something consumable by bytes() construct
            video_file_info["bytes"] = file_stream
            video_file_info["name"] = file_name
            #video_file_info["user_id"] = user_info["id"]
            video_file_info["user_id"] = 1
            video_file_info["upload_date"] = "now"
        video_file_info["bytes"] = self.decode_video(video_file_info["bytes"])
        video_file_info = VideoUpload(**video_file_info)
        return video_file_info

    def decode_video(self, file_stream):
        as_array = []
        for _, b in file_stream.items():
            #print(f"\n\n bytes(b): {bytes(b)} \n\n")
            as_array.append(b)
        print(f"\n\n as_array: {as_array} \n\n")
        as_bytes = bytes(as_array)
        print(f"\n\n as_bytes: {as_bytes} \n\n")
        return as_bytes.decode('utf-8', errors='ignore')

    def set_up(self):
        pass

    def construct_routes(self, app, request):
        pass