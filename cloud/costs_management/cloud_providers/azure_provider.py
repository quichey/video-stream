from .base_provider import BaseProvider

class AzureProvider(BaseProvider):
    CONTEXT = "server"
    PACKAGE_MANAGER = "poetry"
    PACKAGE_PATH = f"{BaseProvider.PATH_PROJECT_ROOT}/{CONTEXT}"
    IMAGE_NAME = f"{CONTEXT}-engine"
    DOCKERFILE = f"{BaseProvider.PATH_PROJECT_DOCKER}/{CONTEXT}/{CONTEXT}.Dockerfile"
    TAG = f"gcr.io/my-project/{CONTEXT}-engine:1.0.0"

    def fetch_services(self):
        # Placeholder: Replace with Azure SDK code to list services/instances
        return [
            {"name": "VM-1", "id": "vm_001"},
            {"name": "AppService-1", "id": "app_001"}
        ]

    def fetch_costs(self, service):
        # Placeholder: Simulate fetching cost
        fake_costs = {
            "vm_001": 150.00,
            "app_001": 45.00,
        }
        return fake_costs.get(service["id"], 0.0)

    def shut_down(self, service):
        print(f"[Azure] Simulating shut down of {service['name']} (id: {service['id']})")
