import argparse

from client.client_deployer import ClientDeployer
from server.server_deployer import ServerDeployer
from util.script_args import get_common_parser


def deploy_instances(machines):
    for deployer in machines:
        deployer.deploy()


if __name__ == "__main__":
    # Build parser using common args
    parser = argparse.ArgumentParser(parents=[get_common_parser()])
    args = parser.parse_args()

    print(f"Cloud-Provider: {args.cloud_provider}")
    print(f"Deployment Environment: {args.env}")
    print(f"Client: {args.client}")
    print(f"Server: {args.server}")

    client_deployer = ClientDeployer(provider_name=args.cloud_provider, env=args.env)
    server_deployer = ServerDeployer(provider_name=args.cloud_provider, env=args.env)

    # If no machines specified, deploy all
    machines = []
    if args.client:
        machines.append(client_deployer)
    if args.server:
        machines.append(server_deployer)
    machines = machines or [client_deployer, server_deployer]

    deploy_instances(machines)
