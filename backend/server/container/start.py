import socket
import os, shutil

import server.util.env as curr_env

# Create a socket object
# AF_INET: IPv4 address family
# SOCK_STREAM: TCP socket type
curr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

temp_pid = hash(curr_socket)
curr_env.set_env("SERVER_PID", temp_pid)


# need to bind the server socket to accept connections from clients
# create a queue of server sockets to be able to facilitate multiple clients
# use Queue class in util
# instantiate with socket hashes as names and values be set to the port that it is bound to