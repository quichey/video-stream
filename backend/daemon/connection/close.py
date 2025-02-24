import socket
import os

import ../util.env

# Create a socket object
# AF_INET: IPv4 address family
# SOCK_STREAM: TCP socket type
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_domain = get_client_domain()

# Define the host and port
host = client_domain["host"]  #loopback address (localhost)
port = client_domain["port"]  # Port number, should be above 1024 to avoid conflicts with well-known ports

# Retrieve client socket from bashrc
config_file = util.get_config_file()
client_socket = util.

# Close the connection
client_socket.close()
s.close()