# Example using Flask and SQLite
from flask import make_response, redirect, url_for
import json

from .Router import Router
from auth.native.native import NativeAuth, NATIVE_AUTH
from auth.google_auth.google_auth import GoogleAuth, GOOGLE_AUTH

"""
Read Flask docs on base code for starting up the Gateway
after understanding it,
place the instantiation of the Cache class
in the base code

TODO: update API's to get comments based on input Video_id
prob just update current comments route since why on 
Earth would someone want just a scan of all comments
soo.. either get video_id from payload or query_str
--- would rather just do payload
- Also update orchestrator/session_manager maybe?
- yes, cause if user swaps videos, need to set page_num to 0
---- think about state_management for this
"""


class ClientRouter(Router):
    NATIVE_AUTH: NativeAuth = NATIVE_AUTH
    GOOGLE_AUTH: GoogleAuth = GOOGLE_AUTH
    """
    don't yet know what i would want in 
    here for ClientRouter, but i'm sure something
    will come up


    TODO: set-up routes to keep track of comments inf scroll w/out needing
    a user to be logged in
    """

    def set_up(self):
        return

    def construct_routes(self, app, request):
        @app.route("/load-session", methods=["POST"])
        def load_session():
            response = make_response("Initial body")
            self.orchestrator.handle_request(request, response)
            return response

        """
        curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0", "video_id": 1}' http://127.0.0.1:5000/video
        """

        # TODO: change methods to "GET" after
        # adding upload_video route
        # and moving session auth to HTTP HEADERS
        @app.route("/video", methods=["POST"])
        def get_video():
            response = make_response("Initial body")
            self.orchestrator.handle_request(request, response)
            return response

        """
        curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0", "video_id": 1}' http://127.0.0.1:5000/video
        """

        # TODO: change methods to "GET" after
        # adding upload_video route
        # and moving session auth to HTTP HEADERS
        # TODO: client side is sending multiple requests
        # handle extra request or get rid of it somehow
        @app.route("/video-upload", methods=["POST"])
        def upload_video():
            response = make_response("Initial body")
            self.orchestrator.handle_request(request, response)
            return response

        @app.route("/upload-profile-pic", methods=["POST"])
        def upload_profile_pic():
            response = make_response("Initial body")
            self.orchestrator.handle_request(request, response)
            return response

        @app.route("/remove-profile-pic", methods=["POST"])
        def remove_profile_pic():
            response = make_response("Initial body")
            self.orchestrator.handle_request(request, response)
            return response

        """
        curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0", "video_id": 1}' http://127.0.0.1:5000/video
        """

        # TODO: change methods to "GET" after
        # adding upload_video route
        # and moving session auth to HTTP HEADERS
        @app.route("/video-list", methods=["POST"])
        def get_video_list():
            response = make_response("Initial body")
            self.orchestrator.handle_request(request, response)
            return response

        # Route to get all items using infinite scroll
        """
        can use different request attributes to make the route url of 
        this infinite scroll paging not weird

        something like request.form['infinite_scroll'] = True
        and then do the listing code
        and otherwise update the DB table or something


        so after thinking, first request should return a larger amount of comments
        than later requests that emulate infinte-scrolling, so that the UI is fluid

        curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0"}' http://127.0.0.1:5000/getcomments
        """

        @app.route("/getcomments", methods=["POST"])
        def read_comments():
            response = make_response("Initial body")
            self.orchestrator.handle_request(request, response)
            return response

        @app.route("/verify-name", methods=["POST"])
        def verify_name():
            response = make_response("Initial body")
            form_data = json.loads(request.data)
            user_name = form_data.get("user_name")
            verified = self.NATIVE_AUTH.verify_user_name_unique(user_name)
            response.data = json.dumps({"verified": verified})
            response.content_type = "application/json"
            return response

        @app.route("/register", methods=["POST"])
        def register():
            response = make_response("Initial body")
            self.orchestrator.handle_request(request, response)
            return response

        @app.route("/login", methods=["POST"])
        def login():
            response = make_response("Initial body")
            self.orchestrator.handle_request(request, response)
            return response

        @app.route("/logout", methods=["POST"])
        def logout():
            response = make_response("Initial body")
            self.orchestrator.handle_request(request, response)
            return response

        @app.route("/google/login", methods=["GET"])
        def google_login():
            redirect_uri = url_for("google_callback", _external=True)
            auth_url = GOOGLE_AUTH.get_authorize_url(redirect_uri)
            return auth_url

        @app.route("/auth/google/callback")
        def google_callback():
            response = make_response("Initial body")
            self.orchestrator.handle_request(request, response)
            return redirect("/")  # send user to React page after login

        # Route to create a new item
        @app.route("/comments", methods=["POST"])
        def create_item():
            # item_data = request.get_json()
            # db = DB()
            # cursor = db.cursor()
            ## TODO: update query
            # query = """
            #    INSERT INTO comments (comment, user_id, date)
            #    VALUES (?,?);
            # """
            # cursor.execute(query,
            #            (item_data['name'], item_data['description']))
            # db.commit()
            # db.close()
            # return jsonify({'message': 'Comment created successfully'}), 201
            pass
