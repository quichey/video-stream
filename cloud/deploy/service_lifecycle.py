import argparse

from client.client_deployer import ClientDeployer
from server.server_deployer import ServerDeployer
from util.script_args import get_common_parser


class ServiceManager:
    """Handles spin-up/shut-down of cloud/dev environment services."""

    def __init__(self, deployers=None):
        """
        services: list of service names or VM identifiers to manage
        """
        self.deployers = deployers or []

    def start(self):
        for dep in self.deployers:
            print(f"Starting service: {dep}")
            dep.start()

    def stop(self):
        for dep in self.deployers:
            dep.stop()


if __name__ == "__main__":
    # Extend the common parser with unique lifecycle args
    parser = argparse.ArgumentParser(parents=[get_common_parser()])
    parser.add_argument(
        "--action",
        choices=["start", "stop"],
        required=True,
        help="Lifecycle action to perform",
    )
    args = parser.parse_args()

    print(f"Cloud-Provider: {args.cloud_provider}")
    print(f"Deployment Environment: {args.env}")
    print(f"Client: {args.client}")
    print(f"Server: {args.server}")
    print(f"Action: {args.action}")

    client_deployer = ClientDeployer(provider_name=args.cloud_provider, env=args.env)
    server_deployer = ServerDeployer(provider_name=args.cloud_provider, env=args.env)

    # If no machines specified, deploy all
    machines = []
    if args.client:
        machines.append(client_deployer)
    if args.server:
        machines.append(server_deployer)
    machines = machines or [client_deployer, server_deployer]

    service_manager = ServiceManager(machines)
    if args.action == "start":
        service_manager.start()
    else:
        service_manager.stop()
