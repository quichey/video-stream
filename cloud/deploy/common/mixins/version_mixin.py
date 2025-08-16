from datetime import datetime
import re

from util.subprocess_helper import run_cmds


class VersionMixin:
    initial_tag = '0.0.0'
    
    def get_latest_version(self, images_archives):

        tags = images_archives
        if not tags:
            print("No tags found... generating initial tag")
            return self.initial_tag
        else:
            return tags[0]


    def generate_timestamped_tag(self, images_archives, bump='patch'):
        """
        Generates a new Docker tag in the format:
        [MAJOR].[MINOR].[PATCH]-dev-YYYY-MM-DD--HH-MM-SS
        """
        #TODO: think about how to connect the providers classes into this
        latest = self.get_latest_version(images_archives)
        latest = latest.split("-")[0]
        major, minor, patch = map(int, latest.split("."))

        if bump == 'patch':
            patch += 1
        elif bump == 'minor':
            minor += 1
            patch = 0
        elif bump == 'major':
            major += 1
            minor = 0
            patch = 0
        else:
            raise ValueError("bump must be 'patch', 'minor', or 'major'")

        timestamp = datetime.utcnow().strftime("%Y-%m-%d--%H-%M-%S")
        return f"{major}.{minor}.{patch}-dev-{timestamp}"