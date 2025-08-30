import datetime
import os
import sys

from api.orchestrator.storage.base_storage import BaseStorage


class LocalStorage(BaseStorage):
    CONTAINER_VIDEOS = "videos"                      # e.g. "videos"
    CONTAINER_IMAGES= "images"

    def store_video(self, file_dir, file_name):
        pass

    def store_image(self, file_dir, file_name):
        pass

    def store_file_in_public(self, file_dir, file_name):
        #TODO: understand what i did in db/Schema/Video/VideoFile.py
        pass

    def get_video_url(self, file_dir, file_name):
        pass

    def get_image_url(self, file_dir, file_name):
        pass
