from abc import ABC, abstractmethod

class Auth(ABC):
    @abstractmethod
    def register(self, user_info):
        pass
    @abstractmethod
    def login(self, user_info):
        pass
    @abstractmethod
    def logout(self, user_info):
        pass