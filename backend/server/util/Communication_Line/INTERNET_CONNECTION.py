import http

ENGINE_SUPPORTED = {"DATABASE": ["MYSQL"], "WEB_BROWSER": ["CHROME"]}


import socket

class INTERNET_CONNECTION(Communication_Line):

    def __init__(self, protocol="HTTP"):
        self.data_verse = DATA_VERSE()
        self.client_base = CLIENT_BASE()

        self.super(entity_class=MACHINE, source_0=data_verse, source_1=client_base)

    # DO MULTITHREADING? MOST WEBAPPS HAVE A SERVER THAT SERVES MULTIPLE CLIENTS
    # WOULD BE NICE TO NOT HAVE TO OPEN UP a bunch of sockets just to serve multiple clients
    # obvious computing restraints requires scaling of either sockets or CPU power something
    # give me more money --- or just a wife and child(s)
    @property
    def chord_function():
        chord = socket.socket("TO_DO_GET_PARAM", "TO_DO_GET_PARAM")
        #TODO  bind socket to TO or FROM IP and then accept messages from TO OR FROM IP
        return chord

    @property
    def socket(self):
        return self.chord

    def send_message(self, giver, receiver):
        if type(giver) == DATA_VERSE:
            break
        elif type(giver) == CLIENT_BASE:
            break

        #add http crap
    
    def add_database(self, db):
        self.data_verse.add_entity(db)
        #update the socket info? maybe not
        # i think if the script has a run function, it continuoulsy polls
        # for messages from both the databases as well as the clients
        pass

    def add_client(self, client):
        self.client_base.add_entity(client)
        pass

    def run(self):
        # listen to and send messages to and fro
        # add http stuff
        # make sure things are secure
        # make sure things are fast
        # make sure connection is steady

        # if a database gets corrupted, do ACID things?
        # let it rest for a while or something
        # clean data
        # and then put it back to work
        pass