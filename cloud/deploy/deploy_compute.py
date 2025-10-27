import argparse

# Assuming these are defined in your environment
from client.client_deployer import ClientDeployer
from server.server_deployer import ServerDeployer

"""
Main script to deploy compute resources (Client and Server applications/containers).
"""


def deploy_instances(machines):
    """Iterates through a list of deployer instances and executes their deploy method."""
    for deployer in machines:
        print(f"\n--- Starting Deployment for {deployer.__class__.__name__} ---")
        deployer.deploy()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deploy Compute Services (Client/Server) to the Cloud/Local environment."
    )

    # Shared Arguments
    parser.add_argument(
        "--cloud_provider",
        default="Azure",
        help="Cloud Provider (e.g., Azure, AWS, GCP)",
    )
    parser.add_argument(
        "--env",
        default="dev",
        choices=["prod", "stage", "dev", "test"],
        help="Deployment environment (prod/stage/dev/test)",
    )

    # Compute Specific Flags
    parser.add_argument("--client", action="store_true", help="Deploy client service")
    parser.add_argument(
        "--server", action="store_true", help="Deploy server service (API/backend)"
    )

    args = parser.parse_args()

    # --- Setup Deployer Instances ---
    client_deployer = ClientDeployer(provider_name=args.cloud_provider, env=args.env)
    server_deployer = ServerDeployer(provider_name=args.cloud_provider, env=args.env)

    # --- Determine Machines to Deploy ---
    default_all = [client_deployer, server_deployer]
    machines = []

    if args.client:
        machines.append(client_deployer)
    if args.server:
        machines.append(server_deployer)

    # If no specific flags were set, deploy all default compute services
    is_specific_flag_set = args.client or args.server
    machines = default_all if not is_specific_flag_set else machines

    if len(machines) == 0:
        print("No compute services specified or available for deployment.")
    else:
        print(f"\nCloud-Provider: {args.cloud_provider}")
        print(f"Deployment Environment: {args.env}")
        print(f"Compute Targets: {[m.__class__.__name__ for m in machines]}")
        deploy_instances(machines)
