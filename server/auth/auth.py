from abc import ABC, abstractmethod
from typing import Literal

from api.util.db_engine import DataBaseEngine
from db.Schema.Models import User


class Auth(ABC, DataBaseEngine):
    @abstractmethod
    def register(self, request, response) -> User | Literal[False]:
        pass

    @abstractmethod
    def login(self, request, response) -> User | Literal[False]:
        pass

    @abstractmethod
    def logout(self, request, response):
        pass
