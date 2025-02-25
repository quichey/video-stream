import socket
import os, shutil

import util.env as env

# Create a socket object
# AF_INET: IPv4 address family
# SOCK_STREAM: TCP socket type
curr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

temp_pid = hash(curr_socket)
env.set_env("SERVER_PID", temp_pid)