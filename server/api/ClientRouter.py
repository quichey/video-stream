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


class ClientRouter():
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


        # Route to get all comments
        @app.route('/blah')
        def html_comments():
            db = DB()
            conn = db.cursor()
            query = """
                SELECT
                    c.comment,
                    u.name as user_name
                FROM
                comments AS c
                LEFT JOIN
                users AS u
                ON c.user_id = u.id;
            """
            conn.execute(query)
            items = conn.fetchall()
            conn.close()
            html = "<u1>"
            for record in items:
                comment = record[0]
                user_name = record[1]
                html += f"<li>@{user_name}: {comment}</li>"
            html += "<ui>"
            return html


        # Route to get all items
        @app.route('/comments', methods=["GET"])
        def read_comments_temp():
            db = DB()
            conn = db.cursor()
            query = """
                SELECT
                    c.comment,
                    u.name as user_name
                FROM
                comments AS c
                LEFT JOIN
                users AS u
                ON c.user_id = u.id;
            """
            conn.execute(query)
            items = conn.fetchall()
            conn.close()
            data = []
            for record in items:
                comment = record[0]
                user_name = record[1]
                data.append({"user_name": user_name, "comment": comment})
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

            form_data = json.loads(request.data)
            # TODO: change later to something like request.form['username']
            user_info = {
                "id": form_data['user_id'],
                "name": form_data['user_name']
            }
            existing_session_info = form_data["token"] if "token" in form_data.keys() else None
            try:
                session_info = cache.get_session(user_info, existing_session_info)
            except SecurityError as security_alarm:
                data = {
                    "status": "error",
                    "msg": security_alarm.msg()
                }
                # later, check Flask docs
                # update with flask framework
                return data
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
            item_data = request.get_json()
            db = DB()
            cursor = db.cursor()
            # TODO: update query
            query = """
                INSERT INTO comments (comment, user_id, date)
                VALUES (?,?);
            """
            cursor.execute(query,
                        (item_data['name'], item_data['description']))
            db.commit()
            db.close()
            return jsonify({'message': 'Comment created successfully'}), 201
