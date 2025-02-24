import os, shutil

# Create a socket object
# AF_INET: IPv4 address family
# SOCK_STREAM: TCP socket type
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_count = os.environ["CLIENT_COUNT"]  # number of users

# TESTING LOCAL SETUP
# Define the host and port
host = os.environ["CLIENT_HOST"]  #loopback address (localhost)
port = os.environ["CLIENT_PORT"]  # Port number, should be above 1024 to avoid conflicts with well-known ports

def get_client_domain():
    return {"host": host, "port": port}
