import http

class MACHINE(Entity):

    def __init__(self, soul="MACHINES", host, port):
        self.host = host
        self.port = port

    @property
    def UNIQUE_ID(self):
        return {"host": self.host, "port": self.port}
    
    @property
    def host(self):
        return self.host
    
    @property
    def port(self):
        return self.port
    
    @property
    def hash(self):
        return f"{self.host}_{self.port}"

import socket

class INTERNET_CONNECTION(Communication_Line):
    # DO MULTITHREADING? MOST WEBAPPS HAVE A SERVER THAT SERVES MULTIPLE CLIENTS
    # WOULD BE NICE TO NOT HAVE TO OPEN UP a bunch of sockets just to serve multiple clients
    # obvious computing restraints requires scaling of either sockets or CPU power something
    # give me more money --- or just a wife and child(s)
    @property
    def chord_function():
        chord = socket.socket("TO_DO_GET_PARAM", "TO_DO_GET_PARAM")
        #TODO  bind socket to TO or FROM IP and then accept messages from TO OR FROM IP
        return chord

