# Example using Flask and SQLite
from flask import Flask, jsonify, request
import mysql.connector

from api.Cache import Cache, SecurityError

"""
Read Flask docs on base code for starting up the Gateway
after understanding it,
place the instantiation of the Cache class
in the base code
"""


app = Flask(__name__)
clients = []

class DB():
    # Database connection configuration
    # TODO: set/get user/pw and get from bashrc
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="new_user",
            password="password",
            database="video_stream"
        )
    
    def cursor(self):
        return self.conn.cursor()


# TODO: add initial route for establishing websocket line of communication
# guessing just add route("/ws") and return status 200 for OK
# probably should check flask or http library for proper headers etc
@app.route('/ws')
def add_client():
    global clients
    clients.append("test")
    return 'STATUS 200 OK'


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
def read_comments():
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
"""
@app.route('/getcomments', methods=["POST"])
def read_comments():
    # request.form['username']
    # the above is an example of getting data from the POST request

    # temp instantiation of Cache object
    cache = Cache()

    session_info = "random_stuff_for_now"
    try:
        session_token = cache.get_session(user_info)
    except SecurityError as security_alarm:
        data = {
            "status": "error"
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

    comment_data = cache.get_comments(session_token)
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

if __name__ == '__main__':
    app.run(debug=True)