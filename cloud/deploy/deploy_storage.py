import argparse
from typing import List, Type

# Import available storage deployers
from server.mysql_db_deployer import MysqlDBDeployer
from server.postgres_db_deployer import PostgresDBDeployer

# Define a flexible base type for deployers
from common.base_db import BaseDBDeployer as StorageDeployerBase

"""
Main script to deploy persistent storage resources (RDBMS, NoSQL, File Storage, etc.).
"""

# Map user-friendly dialect/engine names to the actual Deployer class
RDBMS_DEPLOYER_MAP: dict[str, Type[StorageDeployerBase]] = {
    "mysql": MysqlDBDeployer,
    "postgres": PostgresDBDeployer,
}


def deploy_instances(deployers: List[StorageDeployerBase]):
    """Iterates through a list of deployer instances and executes their deploy method."""
    for deployer in deployers:
        print(f"\n--- Starting Deployment for {deployer.__class__.__name__} ---")
        deployer.deploy()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deploy Persistent Storage Services to the Cloud/Local environment."
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

    # Storage Specific Flags (facilitating combination)
    parser.add_argument(
        "--rdbms",
        type=str,
        choices=RDBMS_DEPLOYER_MAP.keys(),
        help="Deploy the relational database service and specify the engine (e.g., mysql, postgres)",
    )
    parser.add_argument(
        "--filestore",
        action="store_true",
        help="Deploy file storage/blob services (e.g., AWS S3, Azure Blob)",
    )
    parser.add_argument(
        "--warehouse",
        action="store_true",
        help="Deploy data warehousing/analytics services (e.g., Snowflake, AWS Athena)",
    )

    args = parser.parse_args()

    # --- Storage Mapping and Instantiation ---
    storage_deployers: List[StorageDeployerBase] = []

    # RDBMS Deployment Logic
    if args.rdbms:
        DeployerClass = RDBMS_DEPLOYER_MAP[args.rdbms]
        db_deployer = DeployerClass(provider_name=args.cloud_provider, env=args.env)
        storage_deployers.append(db_deployer)

    # File Storage Deployment (Placeholder)
    if args.filestore:
        print(
            "Note: File Store deployment requested but the deployer is not yet configured."
        )

    # Data Warehouse Deployment (Placeholder)
    if args.warehouse:
        print(
            "Note: Data Warehouse deployment requested but the deployer is not yet configured."
        )

    # --- Execution Logic (Default to MySQL if no flags are set) ---
    is_specific_flag_set = args.rdbms or args.filestore or args.warehouse

    if not is_specific_flag_set:
        print(
            "No specific storage services specified. Deploying default RDBMS (MySQL)."
        )
        # Default behavior: If no flags, deploy MySQL
        db_deployer = MysqlDBDeployer(provider_name=args.cloud_provider, env=args.env)
        storage_deployers = [db_deployer]

    # Final Execution
    if len(storage_deployers) == 0:
        print("No storage services specified or configured for deployment.")
    else:
        print(f"\nCloud-Provider: {args.cloud_provider}")
        print(f"Deployment Environment: {args.env}")
        print(f"Storage Targets: {[d.__class__.__name__ for d in storage_deployers]}")
        deploy_instances(storage_deployers)
