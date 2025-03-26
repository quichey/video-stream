# Example using Flask and SQLite
from flask import Flask, jsonify, request
import mysql.connector

from api.Cache import Cache

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
    # request.form["page_size"]
    # request.form["page_number"]
    # use sqlalchemy .limit func iirc
    # also sqlalchemy .offset?
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