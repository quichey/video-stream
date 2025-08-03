from deploy.client.client_deployer import ClientDeployer
from deploy.server.server_deployer import ServerDeployer

def main():
    ClientDeployer().deploy()
    ServerDeployer().deploy()

if __name__ == "__main__":
    main()
