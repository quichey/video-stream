# Example using Flask and SQLite
from flask import jsonify, json

from api.Cache import SecurityError
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
- Also update cache/session_manager maybe?
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
    
    """
    TODO: do re-usable token authentication through HTTP headers instead of payload
    """
    def auth_user(self, request):
        cache = self.cache

        form_data = json.loads(request.data)
        # TODO: change later to something like request.form['username']
        user_info = self.extract_user_info()
        existing_session_info = form_data["token"] if "token" in form_data.keys() else None
        try:
            session_info = cache.get_user_session(user_info, existing_session_info)
        except SecurityError as security_alarm:
            data = {
                "status": "error",
                "msg": security_alarm.msg()
            }
            # later, check Flask docs
            # update with flask framework
            return data
        
        return session_info
    
    """
    TODO: do re-usable token authentication through HTTP headers instead of payload
    """
    def get_session_info(self, request):
        cache = self.cache

        form_data = json.loads(request.data)
        video_info = self.extract_video_info()
        # TODO: change later to something like request.form['username']
        user_info = self.extract_user_info()
        existing_session_info = form_data["token"] if "token" in form_data.keys() else None
        try:
            session_info = cache.get_session(user_info, existing_session_info, video_info)
        except SecurityError as security_alarm:
            data = {
                "status": "error",
                "msg": security_alarm.msg()
            }
            # later, check Flask docs
            # update with flask framework
            return data
        
        return session_info


    def construct_routes(self, app, request):

        """
        curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0", "video_id": 1}' http://127.0.0.1:5000/video
        """
        #TODO: change methods to "GET" after
        # adding upload_video route
        # and moving session auth to HTTP HEADERS
        @app.route('/video', methods=["POST"])
        def get_video():
            # the above is an example of getting data from the POST request

            # temp instantiation of Cache object
            cache = self.cache

            session_info = self.auth_user(request)
            video_info = self.extract_video_info()
            session_info = cache.start_video_session(session_info, video_info)

            video_data = cache.get_video(session_info)
            data = {
                "session_info": session_info,
                "video_data": video_data,
            }
            data = jsonify(data)
            return data

        """
        curl --header "Content-Type: application/json" --request POST --data '{"user_id":"0","user_name":"users_name_0", "video_id": 1}' http://127.0.0.1:5000/video
        """
        #TODO: change methods to "GET" after
        # adding upload_video route
        # and moving session auth to HTTP HEADERS
        @app.route('/video-list', methods=["POST"])
        def get_video_list():
            cache = self.cache

            session_info = self.auth_user(request)

            video_data = cache.get_video_list(session_info)
            data = {
                "session_info": session_info,
                "video_data": video_data,
            }
            data = jsonify(data)
            return data


      
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
            # the above is an example of getting data from the POST request

            # temp instantiation of Cache object
            cache = self.cache

            session_info = self.auth_user(request)
            """
            Handle different cases of different combinations
            of User_id with session_id
            null case: session_id is empty
            then: generate new session --- do i need extra code for this? i don't think so
            case 1: user_id does not match value of session_id
            then: return error code as most likely spoofing attempt
            """

            comment_data = cache.get_comments(session_info)
            data = {
                "session_info": session_info,
                "comment_data": comment_data,
            }
            data = jsonify(data)
            return data


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
