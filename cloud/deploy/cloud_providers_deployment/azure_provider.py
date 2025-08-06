from .base_provider import BaseCloudProvider

class AzureCloudProvider(BaseCloudProvider):
    def get_build_cmd(self, dockerfile, package_path, tag):
        """
        Build and push the Docker image to Azure Container Registry (ACR).
        Assumes the ACR is already created and user is logged in via az.
        """
        acr_name = "myacr"  # Change to your actual ACR name
        full_tag = f"{acr_name}.azurecr.io/{tag}"

        return [
            # Step 1: Build the image locally
            ["docker", "build", "-f", dockerfile, "-t", full_tag, package_path],
            # Step 2: Login to ACR
            ["az", "acr", "login", "--name", acr_name],
            # Step 3: Push the image to ACR
            ["docker", "push", full_tag],
        ]

    def get_run_cmd(self, image_name, tag):
        """
        Deploys a container to Azure Container Apps (ACA).
        Assumes the container image is already pushed to ACR.
        """
        acr_name = "myacr"  # Change to your actual ACR name
        full_tag = f"{acr_name}.azurecr.io/{tag}"
        container_app_name = image_name.lower().replace("_", "-") + "-app"
        resource_group = "myResourceGroup"  # Change to your actual resource group
        environment_name = "myacaenv"       # Change to your actual ACA environment

        return [
            "az", "containerapp", "create",
            "--name", container_app_name,
            "--resource-group", resource_group,
            "--environment", environment_name,
            "--image", full_tag,
            "--target-port", "80",
            "--ingress", "external",
            "--registry-server", f"{acr_name}.azurecr.io",
            "--min-replicas", "1",
            "--max-replicas", "1"
        ]