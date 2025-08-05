from abc import ABC, abstractmethod
import shutil
import os

class BaseProvider(ABC):
    PATH_PROJECT_ROOT = "../.."
    PATH_PROJECT_DOCKER = "../Docker"

    def fetch_services(self):
        pass

    def fetch_costs(self, service):
        pass

    def shut_down(self, service):
        pass