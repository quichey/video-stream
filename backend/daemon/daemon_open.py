import socket
import os, shutil

import constants

# Create a socket object
# AF_INET: IPv4 address family
# SOCK_STREAM: TCP socket type
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port
host = os.environ["CLIENT_HOST"]  #loopback address (localhost)
port = os.environ["CLIENT_PORT"]  # Port number, should be above 1024 to avoid conflicts with well-known ports

# Bind the socket to the host and port
s.bind((host, port))

# Listen for incoming connections (server-side)
s.listen(5) # Maximum number of queued connections

print(f"Server listening on {host}:{port}")

# Accept a connection (server-side)
client_socket, client_address = s.accept()
print(f"Connection from {client_address}")

# Send data
message = "Hello, client!"
client_socket.send(message.encode('utf-8'))

# Receive data
data = client_socket.recv(1024)
print(f"Received: {data.decode('utf-8')}")


# save client socket to bashrc
def set_client_key(host, port):
    config_file = constants.get_config_file()
    backup_file = constants.get_backup_file()
    shutil.copy2(config_file, backup_file)

    lock = constants.get_client_connection_lock(host, port)
    key = constants.set_client_key(host, port)

    with open(config_file, "a") as f:
        f.write(f"\nexport {lock}=\"{key}\"\n")

    print(f"Client Connection Secured")