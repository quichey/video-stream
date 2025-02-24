import socket
import os, shutil

import util.env as env

# Create a socket object
# AF_INET: IPv4 address family
# SOCK_STREAM: TCP socket type
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

temp_pid = 1
env.set_env("server_pid", temp_pid)

# socket object is a dict?

# save metadata of socket object to bash file