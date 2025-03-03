# Example using Flask and SQLite
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('mydatabase.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to get all items
@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return jsonify([dict(item) for item in items])

# Route to create a new item
@app.route('/items', methods=['POST'])
def create_item():
    item_data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (name, description) VALUES (?, ?)',
                   (item_data['name'], item_data['description']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Item created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)