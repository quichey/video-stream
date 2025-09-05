from abc import ABC, abstractmethod

from api.util.db_engine import DataBaseEngine


class Auth(ABC, DataBaseEngine):
    def __init__(self, deployment, *args, **kwargs):
        super().__init__(deployment, args, **kwargs)

    @abstractmethod
    def register(self, request, response):
        pass

    @abstractmethod
    def login(self, request, response):
        pass

    @abstractmethod
    def logout(self, request, response):
        pass
