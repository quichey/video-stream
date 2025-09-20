# cloud/util/script_args.py
import argparse


def parse_common_args():
    parser = argparse.ArgumentParser()

    # cloud provider option
    parser.add_argument("--cloud_provider", default="Azure", help="Cloud Provider")

    parser.add_argument(
        "--env",
        default="dev",
        choices=["prod", "stage", "dev", "test"],
        help="Deployment environment (prod/stage/dev/test)",
    )

    parser.add_argument("--client", action="store_true", help="Target client service")

    parser.add_argument("--server", action="store_true", help="Target server service")

    args = parser.parse_args()
    return args
