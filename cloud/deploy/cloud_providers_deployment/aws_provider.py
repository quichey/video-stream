from dotenv import load_dotenv
import os

from .base_provider import BaseCloudProvider

load_dotenv()

class AWSProvider(BaseCloudProvider):
    def __init__(self, context):
        pass

    def get_build_cmd(self, dockerfile, package_path):
        pass

    def get_run_cmd(self):
        pass

