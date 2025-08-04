import argparse

from client.client_deployer import ClientDeployer
from server.server_deployer import ServerDeployer

"""
If no args given, deploy all machines
"""

def deploy_instances(machines):
    for Deployer in machines:
        Deployer().deploy()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", action="store_true", help="Deploy client service")
    parser.add_argument("--server", action="store_true", help="Deploy server service")

    args = parser.parse_args()

    print(f"Client: {args.client}")
    print(f"Server: {args.server}")
    print("No Machines specified -- Deploying All")

    default_all = [ClientDeployer, ServerDeployer]
    machines = []
    if args.client:
        machines.append(ClientDeployer)
    if args.server:
        machines.append(ServerDeployer)
    machines = default_all if len(machines) == 0 else machines
    deploy_instances(machines)
