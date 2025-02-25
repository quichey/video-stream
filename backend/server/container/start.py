import socket
import os, shutil

import server.util.env as curr_env

# Create a socket object
# AF_INET: IPv4 address family
# SOCK_STREAM: TCP socket type
curr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

temp_pid = hash(curr_socket)
curr_env.set_env("SERVER_PID", temp_pid)