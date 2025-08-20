# Example using Flask and SQLite
from flask import make_response

from .Router import Router

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

        """
        curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0", "video_id": 1}' http://127.0.0.1:5000/video
        """
        #TODO: change methods to "GET" after
        # adding upload_video route
        # and moving session auth to HTTP HEADERS
        @app.route('/video', methods=["POST"])
        def get_video():
            response = make_response("Initial body")
            self.orchestrator.handle_request(request, response)
            return response

        """
        curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0", "video_id": 1}' http://127.0.0.1:5000/video
        """
        #TODO: change methods to "GET" after
        # adding upload_video route
        # and moving session auth to HTTP HEADERS
        #TODO: client side is sending multiple requests
        # handle extra request or get rid of it somehow
        @app.route('/video-upload', methods=["POST"])
        def upload_video():
            response = self.orchestrator.handle_request(request)
            return response

        """
        curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0", "video_id": 1}' http://127.0.0.1:5000/video
        """
        #TODO: change methods to "GET" after
        # adding upload_video route
        # and moving session auth to HTTP HEADERS
        @app.route('/video-list', methods=["POST"])
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
        @app.route('/getcomments', methods=["POST"])
        def read_comments():
            response = make_response("Initial body")
            self.orchestrator.handle_request(request, response)
            return response


        # Route to create a new item
        @app.route('/comments', methods=['POST'])
        def create_item():
            #item_data = request.get_json()
            #db = DB()
            #cursor = db.cursor()
            ## TODO: update query
            #query = """
            #    INSERT INTO comments (comment, user_id, date)
            #    VALUES (?,?);
            #"""
            #cursor.execute(query,
            #            (item_data['name'], item_data['description']))
            #db.commit()
            #db.close()
            #return jsonify({'message': 'Comment created successfully'}), 201
            pass
