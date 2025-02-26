from server.util.INTERNET_CONNECTION import DATABASE, DATA_VERSE, CLIENT_BASE, INTERNET_CONNECTION
import socket
OS_SUPPORTED = ['linux']

class Server(INTERNET_CONNECTION):

    def __init__(self, os = 'linux'):
        if os not in OS_SUPPORTED:
            raise Exception("OS not supported")

        mysql_db = DATABASE(engine="MYSQL")
        mysql_db.add_entity(host="localhost", port=33)
        self.data_verse.add_entity(mysql_db)
    


        

    # Create a socket object
    # AF_INET: IPv4 address family
    # SOCK_STREAM: TCP socket type
    def add_client(self, client_config=None: Address(host="localhost", port=3000)):

        # probably don't need to save this stuff to the bash if the python shell is able to stay up
        # check if python shell can still compute while windows os is in sleep mode
        # possibly can with wsl
        #temp_pid = hash(curr_socket)
        #curr_env.set_env("SERVER_PID", temp_pid)

        clients.append(client_config)

        # bind socket to open portserver_socket.listen(5)

        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
            for host, port in clients:
                try:
                    client_socket, address = server_socket.accept()
                    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
                    client_thread.start()
                    self.db_socket.connect((client_socket))

    
    def connect_to_db(self, db_config= None: Address(host="localhost", port=10)):
        db_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets.append(db_socket)
        self.databases.append(db_config)
        try:
            db_socket.bind((db_config.host, db_config.port))
        except:
            raise Exception("unable to connect to DB")

    def disconnect_from_db(self, db_config):
        pass

    def run():
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
