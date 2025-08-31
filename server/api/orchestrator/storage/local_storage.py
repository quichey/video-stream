import datetime
import os
import sys
import shutil

from api.orchestrator.storage.base_storage import BaseStorage


CLIENT_PUBLIC_FOLDER = "../client/public"
CLIENT_VIDEOS_FOLDER = f"{CLIENT_PUBLIC_FOLDER}/videos"
CLIENT_IMAGES_FOLDER = f"{CLIENT_PUBLIC_FOLDER}/images"

class LocalStorage(BaseStorage):
    CONTAINER_VIDEOS = "videos"                      # e.g. "videos"
    CONTAINER_IMAGES= "images"

    def store_video(self, file_dir, file_name, byte_stream):
        self.store_file_in_public(file_dir, file_name, byte_stream, self.CONTAINER_VIDEOS)
        return True

    def store_image(self, file_dir, file_name, byte_stream):
        self.store_file_in_public(file_dir, file_name, byte_stream, self.CONTAINER_IMAGES)
        #TODO: check if store_file actually worked
        return True

    def store_file_in_public(self, file_dir, file_name, byte_stream, container):
        #TODO: understand what i did in db/Schema/Video/VideoFile.py
        file_location = file_dir
        client_full_file_location = f"{CLIENT_PUBLIC_FOLDER}/{container}/{file_location}"
        client_full_file_name = f"{client_full_file_location}/{file_name}"
        user_folder_exists = os.path.exists(client_full_file_location)
        if not user_folder_exists:
            os.mkdir(client_full_file_location)

        #file_exists = os.path.exists(client_full_file_name)
        #TODO: handle mp4 files
        file = open(client_full_file_name, "wb")
        file.write(byte_stream)
        file.close()
				

    def get_video_url(self, file_dir, file_name):
        pass

    def get_image_url(self, file_dir, file_name):
        pass
