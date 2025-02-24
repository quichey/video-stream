import socket
import os, shutil

import util

# Create a socket object
# AF_INET: IPv4 address family
# SOCK_STREAM: TCP socket type
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# socket object is a dict?

# save metadata of socket object to bash file