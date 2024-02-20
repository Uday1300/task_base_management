from flask import Flask, request, jsonify, session
from database import connect_to_database  
import json

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['JSON_SORT_KEYS'] = False

@app.route('/addtask/', methods=['POST'])
def add_task():
    with connect_to_database() as connection:
        cursor = connection.cursor()
        data = request.form
        user_id = session.get('user_id')
        title = data['title']
        description = data['description']
        due_date = data['dueDate']
        priority = data['priority']
        cursor.execute("""
            INSERT INTO tasks (user_id, title, description, due_date, priority, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (user_id, title, description, due_date, priority))

        connection.commit()

    return jsonify({'message': 'Task added successfully'})