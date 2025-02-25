import socket
import os, shutil

import server.util.env as curr_env

OS_SUPPORTED = ['linux']

class Container():
    sockets = []

    def __init__(self, os = 'linux'):
        if os not in OS_SUPPORTED:
            raise Exception("OS not supported")

    # Create a socket object
    # AF_INET: IPv4 address family
    # SOCK_STREAM: TCP socket type
    def ready_socket():
        curr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        temp_pid = hash(curr_socket)
        # probably don't need to save this stuff to the bash if the python shell is able to stay up
        # check if python shell can still compute while windows os is in sleep mode
        # possibly can with wsl
        curr_env.set_env("SERVER_PID", temp_pid)

        sockets.append(curr_socket)
    
    def remove_socket(socket_hash):
        self.sockets = [s for s in self.sockets if hash(s) is not socket_hash]

        # remove from bash if bash env variables are necessary
        



# need to bind the server socket to accept connections from clients
# create a queue of server sockets to be able to facilitate multiple clients
# use Queue class in util
# instantiate with socket hashes as names and values be set to the port that it is bound to