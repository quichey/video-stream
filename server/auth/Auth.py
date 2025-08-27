from abc import ABC, abstractmethod

class Auth(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @abstractmethod
    def register(self, request, response):
        pass

    @abstractmethod
    def login(self, request, response):
        pass

    @abstractmethod
    def logout(self, request, response):
        pass