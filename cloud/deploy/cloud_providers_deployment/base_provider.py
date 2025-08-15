from abc import ABC, abstractmethod

class BaseCloudProvider(ABC):
    def __init__(self, context):
        self._context = context

    @property
    def context(self):
        return self._context

    @property
    @abstractmethod
    def repo_name(self):
        return self._repo_name

    @repo_name.setter
    def repo_name(self, new_value):
        self._repo_name = new_value

    @property
    @abstractmethod
    def image_tag_base(self):
        return self._image_tag_base

    @image_tag_base.setter
    def image_tag_base(self, new_value):
        self._image_tag_base = new_value

    @property
    @abstractmethod
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, new_value):
        self._tag = new_value

    @abstractmethod
    def get_latest_image(self, image_tag_base, repo_name):
        pass

    @abstractmethod
    def get_build_cmd(self, dockerfile, package_path, tag):
        pass

    @abstractmethod
    def get_run_cmd(self, image_name, tag):
        pass