class SessionBase(ABC):
    @abstractmethod
    def get_token(self) -> str:
        pass

    @abstractmethod
    def get_state(self) -> dict:
        pass

    @abstractmethod
    def update_state(self, key: str, value):
        pass
