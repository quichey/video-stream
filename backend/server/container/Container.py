import socket
import os, shutil

import server.util.env as curr_env
import server.util.DB_Config as DB_Config

OS_SUPPORTED = ['linux']


class Container():
    db_socket = None
    client_sockets = []

    def __init__(self, os = 'linux', db_config= None: DB_Config(host="localhost", port=10)):
        if os not in OS_SUPPORTED:
            raise Exception("OS not supported")
        
        db_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.db_socket = db_socket
        try:
            db_socket.bind((db_config.host, db_config.port))
        except:
            raise Exception("unable to connect to DB")

    # Create a socket object
    # AF_INET: IPv4 address family
    # SOCK_STREAM: TCP socket type
    def listen_to_client(self, client_config=None: DB_Config(host="localhost", port=3000)):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # probably don't need to save this stuff to the bash if the python shell is able to stay up
        # check if python shell can still compute while windows os is in sleep mode
        # possibly can with wsl
        #temp_pid = hash(curr_socket)
        #curr_env.set_env("SERVER_PID", temp_pid)

        sockets.append(client_socket)

        # bind socket to open port
        for i in [0:3000]:
            try:
                self.db_socket.connect((client_socket))
                
    
    def remove_socket(socket_hash):
        self.sockets = [s for s in self.sockets if hash(s) is not socket_hash]

        # remove from bash if bash env variables are necessary

"""
import socket
import threading

def handle_client(client_socket):
    # Handle client connection
    client_socket.send(b"Hello, client!")
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 12345))
server_socket.listen(5)

while True:
    client_socket, address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
"""