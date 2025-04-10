# Example using Flask and SQLite
from flask import Flask, jsonify, json
import mysql.connector

from api.Cache import Cache, SecurityError

"""
Read Flask docs on base code for starting up the Gateway
after understanding it,
place the instantiation of the Cache class
in the base code
"""


class AdminRouter():
    def __init__(self, app, cache, request):
        self.cache = cache

        def get_route_signatures(self):
            signatures = [
                (self.html_comments, "/blah", ["GET"]),
                (self.add_client, "/ws", ["GET"]),
                (self.read_comments_temp, "/comments", ["GET"]),
                (self.read_comments, "/getcomments", ["POST"]),
            ]

            return signatures

       
        """
        admin util cmd to clear user session for testing

        seems to be very difficult --- maybe lets
        setup just http routes that authenticate that the 
        sender is an admin
        then do the thingys
        """
        @app.route("/user/session", methods=["DELETE"])
        def clear_user_session():
            # TODO: for now, block any access till
            # I research good way to authenticate
            if True:
                return
            user_info = "blah"
            session_info = "blah"
            cache.clear_user_session(user_info, session_info)
            return "something"


        # TODO: add initial route for establishing websocket line of communication
        # guessing just add route("/ws") and return status 200 for OK
        # probably should check flask or http library for proper headers etc
        @app.route('/ws')
        def add_client():
            global clients
            clients.append("test")
            return 'STATUS 200 OK'
