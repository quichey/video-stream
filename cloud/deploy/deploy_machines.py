from client.ClientDeployer import ClientDeployer
from server.ServerDeployer import ServerDeployer
import sys
from pathlib import Path

def main():
    # Determine deploy environment from CLI arg or default
    deploy_env = sys.argv[1] if len(sys.argv) > 1 else "local"

    # Assuming this script is run from project root
    project_root = Path(__file__).parent.resolve()

    print(f"Starting deployment in '{deploy_env}' environment...\n")

    # Deploy Client
    print("=== Deploying Client ===")
    client_deployer = ClientDeployer(project_root=project_root, deploy_env=deploy_env)
    client_deployer.deploy()

    print("\n=== Deploying Server ===")
    server_deployer = ServerDeployer(project_root=project_root, deploy_env=deploy_env)
    server_deployer.deploy()

    print("\nDeployment finished successfully!")

if __name__ == "__main__":
    main()
