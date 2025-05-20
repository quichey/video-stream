from dataclasses import dataclass
from typing import List

from db.Schema import Video

"""
should prob save the file location in the
videos table or bashrc since the Seed installation
is a separate process from the api gateway daemon

TODO: store file locations in file_dir col of videos table
TODO: plan out good data structures for this file/module/class
"""

ROOT_FOLDER = "db/assets"



class VideoFileManager():
	def __init__(self):
		pass
	
	#TODO: rename these
	"""
	Plan to use these 4 funcs for API and user uploading a video
	"""
	def store_video(self, video_record):
		self.videos[video_record.id]
		file_location = self.determine_file_location()
		pass

	def read_video(self, video_id):
		pass

	def update_video(self, video_id, file_location, file_name=None):
		pass

	def delete_video(self, video_id):
		pass


	def determine_file_location(self, video_id, user_id):
		user_folder = f"{user_id}"
		video = self._fetch_video(video_id)
		video.file_location = user_folder
		return user_folder

	def save_file_location(self, video_id, file_location, video_record):
		video_record.file_dir = file_location
		full_file_location = f"{ROOT_FOLDER}/{file_location}"
		user_folder_exists = pass
		if not user_folder_exists:
			#TODO: create user_folder
		#TODO: upload video file to folder?/ bash cp file to folder?
		file_exists = pass
		if file_exists:
			return
		#NOTE: do not need to do sqlalchemy stuff cause session in Seed will handle once 
		# it flushes
		pass

	def load_videos(self, video_records: List[Video]):
		self.video_records = video_records
		for one_video_record in video_records:
			file_location = self.determine_file_location(one_video_record.id, one_video_record.user_id)
			self.save_file_location(one_video_record.id, file_location, one_video_record)
		
		return