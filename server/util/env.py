from dotenv import load_dotenv
import os


def load_server_env():
    load_dotenv()
    return


def load_providers_env(provider="azure"):
    deploy_env = os.environ.get("DEPLOYMENT")
    # TODO: use path of this file?
    if deploy_env == "local":
        load_dotenv(f"../cloud/providers/{provider}/.env")
    else:
        load_dotenv(f"env/{provider}/.env")
    load_authorizors_env()
    return


def load_authorizors_env():
    load_dotenv("../cloud/providers/gcp/.env")
