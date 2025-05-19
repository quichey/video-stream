from dataclasses import dataclass

@dataclass
class VideoFile():
	file_name = str
	file_location = str
	video_id = int


class VideoFileManager():
	def __init__(self):
		self.videos = {}
		pass
	

	def create_video(self, file_name, file_location):
		pass

	def read_video(self, video_id):
		pass

	def update_video(self, video_id, file_location, file_name=None):
		pass

	def delete_video(self, video_id):
		pass