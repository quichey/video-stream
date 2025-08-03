from client.client_deployer import ClientDeployer
from server.server_deployer import ServerDeployer

def main():
    ClientDeployer().deploy()
    ServerDeployer().deploy()

if __name__ == "__main__":
    main()
