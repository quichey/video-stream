from dataclasses import dataclass

"""
should prob save the file location in the
videos table or bashrc since the Seed installation
is a separate process from the api gateway daemon

TODO: store file locations in file_dir col of videos table
TODO: plan out good data structures for this file/module/class
"""

ROOT_FOLDER = "db/assets"

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

	def update_ids(self, video_records):
		pass

	def determine_file_location(self, video_meta_data):
		pass

	def save_file_location(self, video_id, file_location):
		pass