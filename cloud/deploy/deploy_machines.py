import argparse

from client.client_deployer import ClientDeployer
from server.server_deployer import ServerDeployer
from server.mysql_db_deployer import MysqlDBDeployer

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
    parser.add_argument(
        "--env",
        default="dev",
        choices=["prod", "stage", "dev", "test"],
        help="Deployment environment (prod/stage/dev/test)",
    )

    parser.add_argument("--client", action="store_true", help="Deploy client service")
    parser.add_argument("--server", action="store_true", help="Deploy server service")
    parser.add_argument("--db", action="store_true", help="Deploy db service")

    args = parser.parse_args()

    print(f"Cloud-Provider: {args.cloud_provider}")
    print(f"Deployment Environment: {args.env}")

    print(f"Client: {args.client}")
    print(f"Server: {args.server}")
    print(f"DB: {args.db}")
    if args.client is None and args.server is None and args.db is None:
        print("No Machines specified -- Deploying All")

    client_deployer = ClientDeployer(provider_name=args.cloud_provider, env=args.env)
    server_deployer = ServerDeployer(provider_name=args.cloud_provider, env=args.env)
    db_deployer = MysqlDBDeployer(provider_name=args.cloud_provider, env=args.env)

    default_all = [client_deployer, server_deployer, db_deployer]
    machines = []
    if args.client:
        machines.append(client_deployer)
    if args.server:
        machines.append(server_deployer)
    if args.db:
        machines.append(db_deployer)
    machines = default_all if len(machines) == 0 else machines
    deploy_instances(machines)
