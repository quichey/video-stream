from abc import ABC, abstractmethod


class BaseStorage(ABC):
    CONTAINER_VIDEOS = "videos"                      # e.g. "videos"
    CONTAINER_IMAGES= "images"

    @abstractmethod
    def get_video_url(self, file_dir, file_name):
        pass

    @abstractmethod
    def get_image_url(self, file_dir, file_name):
        pass

    @abstractmethod
    def store_video(self, file_dir, file_name):
        pass

    @abstractmethod
    def store_image(self, file_dir, file_name):
        pass