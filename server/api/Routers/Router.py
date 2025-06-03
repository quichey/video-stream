from flask import json

"""
Thinking maybe have this class to handle any common Flask
Logic that I see in ClientRouter and AdminRouter
"""

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
        print(f"\n\n reached extract_video_file_info \n\n")
        form_data = json.loads(self.request.data)
        video_file_info = {}
        if "file" in form_data:
            file = form_data['file']
            print(f"file: {file}")
            video_file_info["stream"] = file
        video_file_info["stream"] = self.decode_video(video_file_info["stream"])
        return video_file_info

    def decode_video(self, file_stream):
        as_bytes = bytes(file_stream)
        return as_bytes.decode('utf-8', errors='ignore')

    def set_up(self):
        pass

    def construct_routes(self, app, request):
        pass