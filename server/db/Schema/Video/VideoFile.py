from typing import List
import os
import shutil

from db.Schema import Video

"""
should prob save the file location in the
videos table or bashrc since the Seed installation
is a separate process from the api gateway daemon

TODO: store file locations in file_dir col of videos table
TODO: plan out good data structures for this file/module/class
"""
SERVER_ASSETS_FOLDER = "db/assets"
CLIENT_PUBLIC_FOLDER = "../client/public/videos"



class VideoFileManager():
	def __init__(self):
		pass
	
	#TODO: rename these
	"""
	Plan to use these 4 funcs for API and user uploading a video
	"""
	def store_video_old(self, video_record):
		pass

	def read_video(self, video_id):
		pass

	def update_video(self, video_id, file_location, file_name=None):
		pass

	def delete_video(self, video_id):
		pass

	"""
	TODO?: maybe at some point clean up these functions
	looks messy and note quite sure how to formulate
	tidier writing right now
	"""

	def determine_file_location(self, video_record):
		user_id = video_record.user_id
		user_folder = f"{user_id}"
		return user_folder

	def store_video(self, video_record, seeding_db=True, byte_stream=None):
		file_location = self.determine_file_location(video_record)
		server_full_file_location = f"{SERVER_ASSETS_FOLDER}"
		client_full_file_location = f"{CLIENT_PUBLIC_FOLDER}/{file_location}"
		server_full_file_name = f"{server_full_file_location}/{video_record.file_name}"
		client_full_file_name = f"{client_full_file_location}/{video_record.file_name}"
		print(f"\n\n server_full_file_location: {server_full_file_location}\n\n")
		print(f"\n\n client_full_file_location: {client_full_file_location}\n\n")
		print(f"\n\n server_full_file_name: {server_full_file_name}\n\n")
		print(f"\n\n client_full_file_name: {client_full_file_name}\n\n")

		video_record.file_dir = file_location
		user_folder_exists = os.path.exists(client_full_file_location)
		if not user_folder_exists:
			os.mkdir(client_full_file_location)

		#print(f"\n\n full_file_location: {full_file_location} \n\n")
		#print(f"\n\n full_file_name: {full_file_name} \n\n")
		file_exists = os.path.exists(client_full_file_name)
		if not file_exists:
			if seeding_db:
				source_path = server_full_file_name
				shutil.copy(source_path, client_full_file_location)
			#TODO: handle saving file from user upload
			else:
				#TODO: handle mp4 files
				file = open(client_full_file_name, "wb")
				"""
				as_str = str(byte_stream)
				print(f"\n\n length of as_str: {len(as_str)} \n\n")
				# take out 
				str_to_remove = "Create videos with https://clipchamp.com/en/video-editor - free online video editor, video compressor, video converter."
				new_text = as_str.replace(str_to_remove, "")
				print(f"\n\n length of new_text: {len(new_text)} \n\n")
				file.write(new_text)
				"""
				print(f"\n\n length of byte_stream: {len(byte_stream)} \n\n")
				file.write(byte_stream)
				file.close()
				
				

		#NOTE: do not need to do sqlalchemy stuff cause session in Seed will handle once 
		# it flushes
		return

	def load_videos(self, video_records: List[Video]):
		self.video_records = video_records
		for one_video_record in video_records:
			self.store_video(one_video_record)
		
		return