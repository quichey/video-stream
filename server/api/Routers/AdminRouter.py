# Example using Flask and SQLite
from flask import Flask, jsonify, json
import os
from dotenv import load_dotenv

from api.orchestrator.Cache import Cache
from .Router import Router
from api.util.error_handling import SecurityError

"""
Read Flask docs on base code for starting up the Gateway
after understanding it,
place the instantiation of the Cache class
in the base code
"""


class AdminRouter(Router):
    def set_up(self):
        load_dotenv()
        self.admin_secret = os.getenv("FLASK_ADMIN_SECRET")
        return

    def construct_routes(self, app, request):

       
        """
        admin util cmd to clear user session for testing

        seems to be very difficult --- maybe lets
        setup just http routes that authenticate that the 
        sender is an admin
        then do the thingys


        
        curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0"}' http://127.0.0.1:5000/getcomments
        curl --header "Content-Type: application/json" --request DELETE --data '{"user_id":"0","user_name":"users_name_0", "auth_key": "something"}' http://127.0.0.1:5000/admin/user/session
        curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0"}' http://127.0.0.1:5000/getcomments

        """
        @app.route("/admin/user/session", methods=["DELETE"])
        def clear_user_session_admin():
            # TODO: for now, block any access till
            # I research good way to authenticate
            form_data = json.loads(request.data)
            auth_key = form_data['auth_key']
            if str(auth_key) != str(self.admin_secret):
                raise SecurityError("Admin Privileges Required")
            user_info = self.extract_user_info()
            self.cache.clear_user_session_admin(user_info)
            return "something"


        # TODO: add initial route for establishing websocket line of communication
        # guessing just add route("/ws") and return status 200 for OK
        # probably should check flask or http library for proper headers etc
        @app.route('/ws')
        def add_client():
            global clients
            clients.append("test")
            return 'STATUS 200 OK'
