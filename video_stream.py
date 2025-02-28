import socket.socket
import HTTP
import requests

SERVER_ADDRESS = ('localhost', 20)

def run():
    server_class=HTTPServer, handler_class=BaseHTTPRequestHandler
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
    #wire = socket.socket("blah")
    # bind socket to heroku host address
    # probably just localhost


    #db_params = []
    # bind socket to db for when doing data stuff
    # 


    list_of_clients = []
    # maybe make html.py later if reasonable for scaling
    def client_message_handler(request_url):
        # send HTML based off of the request url
        # right now just one url
        
        html =  "<script> Hello </script>"


        #r = requests.get('https://api.github.com/events')
        # i think don't need this yet since there is only one request, which is always
        # sent by the client to the hosted domain

        # socket.send or something
            
    while True:
        #poll for messages
        # socket.listen or something
        #

    return

# since it's a heroku thing, i'm pretty sure they'll just shut down the whole machine
# don't bother with closing code?