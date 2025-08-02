from client.client_deployer import ClientDeployer
from server.server_deployer import ServerDeployer

def main():
    print("Starting deployment")

    client = ClientDeployer()
    server = ServerDeployer()

    client.deploy()
    server.deploy()

if __name__ == "__main__":
    main()
