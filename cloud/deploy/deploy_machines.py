import argparse

from client.client_deployer import ClientDeployer
from server.server_deployer import ServerDeployer

"""
If no args given, deploy all machines
"""

def deploy_instances(machines):
    for Deployer in machines:
        Deployer.deploy()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # cloud provider option
    parser.add_argument("--cloud_provider", default="Azure", help="Cloud Provider")

    parser.add_argument("--client", action="store_true", help="Deploy client service")
    parser.add_argument("--server", action="store_true", help="Deploy server service")

    args = parser.parse_args()

    print(f"Cloud-Provider: {args.cloud_provider}")

    print(f"Client: {args.client}")
    print(f"Server: {args.server}")
    print("No Machines specified -- Deploying All")

    client_deployer = ClientDeployer(provider_name=args.cloud_provider)
    server_deployer = ServerDeployer(provider_name=args.cloud_provider)

    default_all = [client_deployer, server_deployer]
    machines = []
    if args.client:
        machines.append(client_deployer)
    if args.server:
        machines.append(server_deployer)
    machines = default_all if len(machines) == 0 else machines
    deploy_instances(machines)
