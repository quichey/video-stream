from abc import ABC, abstractmethod

from api.util.db_engine import DataBaseEngine


class Auth(ABC, DataBaseEngine):
    @abstractmethod
    def register(self, request, response):
        pass

    @abstractmethod
    def login(self, request, response):
        pass

    @abstractmethod
    def logout(self, request, response):
        pass
