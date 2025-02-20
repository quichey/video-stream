import socket
import os

# Create a socket object
# AF_INET: IPv4 address family
# SOCK_STREAM: TCP socket type
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port
host = os.environ["CLIENT_HOST"]  #loopback address (localhost)
port = os.environ["CLIENT_PORT"]  # Port number, should be above 1024 to avoid conflicts with well-known ports

# Retrieve client socket from bashrc
client_socket = None

# Close the connection
client_socket.close()
s.close()