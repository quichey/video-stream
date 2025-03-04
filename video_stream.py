# Example using Flask and SQLite
from flask import Flask, jsonify, request
import mysql.connector


app = Flask(__name__)

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


# Route to get all items
@app.route('/comments', methods=['GET'])
def get_items():
    db = DB()
    conn = db.cursor()
    query = """
        SELECT
            c.comment,
            u.name
        FROM
        comments AS c
        LEFT JOIN
        users AS u
        ON c.user_id = u.id;
    """
    items = conn.execute(query).fetchall()
    data = jsonify([dict(item) for item in items])
    conn.close()
    return data

# Route to create a new item
@app.route('/comments', methods=['POST'])
def create_item():
    item_data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    # TODO: update query
    query = """
        INSERT INTO comments (comment, user_id, date)
        VALUES (?,?);
    """
    cursor.execute(query,
                   (item_data['name'], item_data['description']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Comment created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)