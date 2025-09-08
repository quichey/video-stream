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

    """
    Should i check the request user cookie against DB everytime?
    Or create instances of the Auths instead of singleton?
    kind of want to make this func not abstractmethod
    but 3rd party auths use refresh token
    I do not do this with NativeAuth,
    instead with NativeAuth, just creates a new UserSession if 
    expired cookie doesn't show up
    """

    @abstractmethod
    def authorize(self, request, response) -> bool:
        pass
