from abc import ABC, abstractmethod

class BaseProvider(ABC):
    PATH_PROJECT_ROOT = "../.."
    PATH_PROJECT_DOCKER = "../Docker"

    @abstractmethod
    def fetch_services(self):
        """Fetch a list of running services/instances."""
        pass

    @abstractmethod
    def fetch_costs(self, service):
        """Fetch the cost details for a specific service."""
        pass

    @abstractmethod
    def shut_down(self, service):
        """Shut down the given service/instance."""
        pass
