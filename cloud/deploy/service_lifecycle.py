# cloud/deploy/service_lifecycle.py
from cloud.providers.azure import start_vm, stop_vm  # your Azure helper functions


class ServiceManager:
    """Handles spin-up/shut-down of cloud/dev environment services."""

    def __init__(self, services=None):
        """
        services: list of service names or VM identifiers to manage
        """
        self.services = services or []

    def start(self):
        for svc in self.services:
            print(f"Starting service: {svc}")
            start_vm(svc)  # replace with actual Azure API call or deploy logic

    def stop(self):
        for svc in self.services:
            print(f"Stopping service: {svc}")
            stop_vm(svc)  # replace with actual Azure API call or deploy logic
